# ===========================Data for access report
# http://127.0.0.1:8000/skf/report_sales/acreportData?c_id=SKF&dateFrom=2016-06-01&dateTo=2016-06-05&branch=
# http://c003.cloudapp.net/skf/report_sales/acreportData?c_id=SKF&dateFrom=2016-06-01&dateTo=2016-06-05&branch=170
# Region|Area|Territory|Market|Product ID | Product Name| TP| Stock| Catetory A/B/C| Qty
def acreportData():
    c_id=request.vars.c_id
    dateFrom=request.vars.dateFrom
    dateTo=request.vars.dateTo
    branch=request.vars.branch
    dateFlag=True
    try:
        dateFrom=datetime.datetime.strptime(str(dateFrom),'%Y-%m-%d')
        dateTo=datetime.datetime.strptime(str(dateTo),'%Y-%m-%d')
        date_to_m=dateTo + datetime.timedelta(days = 1)
        if dateFrom > dateTo :
            dateFlag=False
    except:
        dateFlag=False
     
    if dateFlag==False:
        return "Invalid Date"
    
    
    
    qset=db()
    qset=qset(db.sm_invoice.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.cid==db.sm_invoice.cid)
    qset=qset(db.sm_depot_stock_balance.cid==db.sm_invoice.cid)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_invoice.item_id)
    qset=qset(db.sm_depot_stock_balance.batch_id==db.sm_invoice.batch_id)
    qset=qset(db.sm_invoice.status=='Invoiced')    
    qset=qset((sm_invoice.invoice_date >= dateFrom) & (sm_invoice.invoice_date < date_to_m))
    qset=qset(db.sm_invoice.depot_id==branch)
    
    records=qset.select(db.sm_invoice.level2_id,db.sm_invoice.level2_name,db.sm_invoice.level1_id,db.sm_invoice.level1_name,db.sm_invoice.level0_id,db.sm_invoice.level0_name,db.sm_invoice.market_id,db.sm_invoice.market_name, db.sm_invoice.item_id,db.sm_invoice.item_name,db.sm_invoice.actual_tp, db.sm_invoice.category_id,db.sm_invoice.batch_id,db.sm_depot_stock_balance.quantity,db.sm_invoice.quantity.sum(), groupby=db.sm_invoice.level1_id|db.sm_invoice.level2_id|db.sm_invoice.level3_id|db.sm_invoice.market_id|db.sm_invoice.item_id|db.sm_invoice.batch_id, orderby= db.sm_invoice.level1_id|db.sm_invoice.level2_id|db.sm_invoice.level3_id|db.sm_invoice.market_id|db.sm_invoice.item_id|db.sm_invoice.batch_id)
#     return db._lastsql
    report_str=''
    for record in records:
        region=record[db.sm_invoice.level1_id]
        region_name=record[db.sm_invoice.level1_name]
        area=record[db.sm_invoice.level2_id]
        area_name=record[db.sm_invoice.level2_name]
        territory=record[db.sm_invoice.level3_id]
        territory_name=record[db.sm_invoice.level3_name]
        market=record[db.sm_invoice.market_id]
        market_name=record[db.sm_invoice.market_name]
        item=record[db.sm_invoice.item_id]
        item_name=record[db.sm_invoice.item_name]
        item_batch=record[db.sm_invoice.batch_id]
        tP=record[db.sm_invoice.actual_tp]
        catetory=record[db.sm_invoice.category_id]
        qty=record[db.sm_invoice.quantity.sum()]
        stock=record[db.sm_depot_stock_balance.quantity]
        if report_str=='':
            report_str=str(region)+'|'+str(region_name)+'|'+str(area)+str(area_name)+'|'+str(territory)+'|'+str(territory_name)+'|'+str(market)+'|'+str(market_name)+'|'+str(item)+'|'+str(item_name)+'|'+str(item_batch)+'|'+str(tP)+'|'+str(stock)+'|'+str(catetory)+'|'+str(qty)

        else:
            report_str=report_str+'<rdrd>'+str(region)+'|'+str(region_name)+'|'+str(area)+str(area_name)+'|'+str(territory)+'|'+str(territory_name)+'|'+str(market)+'|'+str(market_name)+'|'+str(item)+'|'+str(item_name)+'|'+str(item_batch)+'|'+str(tP)+'|'+str(stock)+'|'+str(catetory)+'|'+str(qty)

        
        
        
        


    return report_str




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
#    task_id='rm_analysis_view'
#    access_permission=check_role(task_id)
#    if (access_permission==False ):
#        session.flash='Access is Denied'
#        redirect (URL('default','home'))
    
    response.title='Report'
    
    c_id=session.cid
    
    search_form =SQLFORM(db.sm_search_date)
    
    
    
    
#    =============Sales btn Start Nadira===========
    btn_list_sales=request.vars.btn_list_sales
    btn_customer_wise_sales=request.vars.btn_customer_wise_sales
    btn_item_wise_batch_sales=request.vars.btn_item_wise_batch_sales
    btn_item_wise_sales=request.vars.btn_item_wise_sales
    btn_msowiseS=request.vars.btn_msowiseS
    btn_msowiseSDLoad=request.vars.btn_msowiseSDLoad

    
    btn_catMSOwiseS=request.vars.btn_catMSOwiseS
    btn_catDPwiseS=request.vars.btn_catDPwiseS
    btn_catDPwiseSD=request.vars.btn_catDPwiseSD
    btn_dpwiseSD=request.vars.btn_dpwiseSD
    btn_dpwiseSDD=request.vars.btn_dpwiseSDD
    btn_customerProductS=request.vars.btn_customerProductS
    btn_customerProductSD=request.vars.btn_customerProductSD
    btn_productS=request.vars.btn_productS
    btn_productSD=request.vars.btn_productSD
    btn_productSwithoutBonus=request.vars.btn_productSwithoutBonus
    btn_productSwithoutBonusD=request.vars.btn_productSwithoutBonusD
    
   
    btn_customerProductSIncludinBonus=request.vars.btn_customerProductSIncludinBonus
    btn_customerProductSIncludinBonusD=request.vars.btn_customerProductSIncludinBonusD
    
    btn_customerProductSExcludinBonus=request.vars.btn_customerProductSExcludinBonus
    btn_customerProductSExcludinBonusD=request.vars.btn_customerProductSExcludinBonusD
    
    btn_customerInvoiceProductS=request.vars.btn_customerInvoiceProductS
    btn_customerInvoiceProductSwithBonus=request.vars.btn_customerInvoiceProductSwithBonus
    btn_customerInvoiceProductSwithoutBonus=request.vars.btn_customerInvoiceProductSwithoutBonus
    btn_customerInvoiceProductSD=request.vars.btn_customerInvoiceProductSD
    btn_customerInvoiceProductSwithBonusD=request.vars.btn_customerInvoiceProductSwithBonusD
    btn_customerInvoiceProductSwithoutBonusD=request.vars.btn_customerInvoiceProductSwithoutBonusD
    
    
    
    btn_productInvoicewiseSD=request.vars.btn_productInvoicewiseSD 
    btn_productInvoicewiseSDwithBonus=request.vars.btn_productInvoicewiseSDwithBonus
    btn_productInvoicewiseSDwithoutBonus=request.vars.btn_productInvoicewiseSDwithoutBonus
    
    btn_productInvoicewiseSDD=request.vars.btn_productInvoicewiseSDD 
    btn_productInvoicewiseSDwithBonusD=request.vars.btn_productInvoicewiseSDwithBonusD
    btn_productInvoicewiseSDwithoutBonusD=request.vars.btn_productInvoicewiseSDwithoutBonusD
    
    
    btn_invoicewiseSD=request.vars.btn_invoicewiseSD
    btn_invoicewiseSDLoad=request.vars.btn_invoicewiseSDLoad
    
    btn_summary=request.vars.btn_summary
    btn_summaryD=request.vars.btn_summaryD
    
    btn_SalesClosingStockS=request.vars.btn_SalesClosingStockS
    btn_SalesClosingStockSD=request.vars.btn_SalesClosingStockSD
    btn_SalesClosingStockSB=request.vars.btn_SalesClosingStockSB
    btn_SalesClosingStockSBD=request.vars.btn_SalesClosingStockSBD
    
#    ============Order=========================
# Nadira
    btn_list_oderdetail=request.vars.btn_list_oderdetail
    btn_list_oderdSummary_spowise=request.vars.btn_list_oderdSummary_spowise
    btn_list_oderdSummary_spowiseDdate=request.vars.btn_list_oderdSummary_spowiseDdate
    btn_item_wise_sales_sheet=request.vars.btn_item_wise_sales_sheet
#   ===  
    
    btn_item_wise_sale_detail=request.vars.btn_item_wise_sale_detail
    btn_item_wise_sale_detail_land=request.vars.btn_item_wise_sale_detail_land
    btn_invoice_wise_sale_detail=request.vars.btn_invoice_wise_sale_detail
    btn_invoice_wise_sale_detailD=request.vars.btn_invoice_wise_sale_detailD
    
    
    btn_customer_wise_sale_detail=request.vars.btn_customer_wise_sale_detail
    btn_customer_wise_sale_detailP=request.vars.btn_customer_wise_sale_detailP
    btn_customer_wise_sale_detailPD=request.vars.btn_customer_wise_sale_detailPD
    
    btn_mso_wise_sale_detail=request.vars.btn_mso_wise_sale_detail
    btn_mso_wise_sale_detailD=request.vars.btn_mso_wise_sale_detailD
    
    btn_dp_wise_sale_detail=request.vars.btn_dp_wise_sale_detail
    btn_dp_wise_sale_detailD=request.vars.btn_dp_wise_sale_detailD
    
    
                                       
    btn_customer_nformation=request.vars.btn_customer_nformation
    btn_customer_nformationD=request.vars.btn_customer_nformationD
    
    
    btn_item_wise_sale_detailDLoad=request.vars.btn_item_wise_sale_detailDLoad
    
    btn_causeofrtn=request.vars.btn_causeofrtn
    btn_causeofrtnDLoad=request.vars.btn_causeofrtnDLoad
    
    btn_DP_wise_sale_ss=request.vars.btn_DP_wise_sale_ss
    btn_DP_wise_sale_ssD=request.vars.btn_DP_wise_sale_ssD
    
    
    btn_sComparision=request.vars.btn_sComparision
    btn_sComparisionD=request.vars.btn_sComparisionD
    
    
    
#     Sales Comparision========================
    btn_salesComparisionNational=request.vars.btn_salesComparisionNational
    btn_salesComparisionNationalD=request.vars.btn_salesComparisionNationalD
    btn_salesComparisionRsm=request.vars.btn_salesComparisionRsm
    btn_salesComparisionRsmD=request.vars.btn_salesComparisionRsmD
    btn_salesComparisionFm=request.vars.btn_salesComparisionFm
    btn_salesComparisionFmD=request.vars.btn_salesComparisionFmD
    btn_salesComparisionTr=request.vars.btn_salesComparisionTr
    btn_salesComparisionTrD=request.vars.btn_salesComparisionTrD
    
    btn_salesComparisionTrDetail=request.vars.btn_salesComparisionTrDetail
    btn_salesComparisionTrDetailD=request.vars.btn_salesComparisionTrDetailD
    btn_salesComparisionFmDetail=request.vars.btn_salesComparisionFmDetail
    btn_salesComparisionFmDetailD=request.vars.btn_salesComparisionFmDetailD
    btn_salesComparisionRsmDetail=request.vars.btn_salesComparisionRsmDetail
    btn_salesComparisionRsmDetailD=request.vars.btn_salesComparisionRsmDetailD
    btn_salesComparisionMarketDetail=request.vars.btn_salesComparisionMarketDetail
#     =======================================
    
#     return btn_causeofrtn
    #     ================================================Sales Nadira==========================================================================================
#     Nadira
    if (btn_list_sales or btn_customer_wise_sales or btn_item_wise_batch_sales or btn_item_wise_sales or btn_list_oderdetail or btn_list_oderdSummary_spowise or btn_list_oderdSummary_spowiseDdate or btn_item_wise_sale_detail or btn_item_wise_sale_detailDLoad or btn_item_wise_sale_detail_land or btn_invoice_wise_sale_detail or btn_invoice_wise_sale_detailD or btn_customer_wise_sale_detail or btn_customer_wise_sale_detailP or btn_customer_wise_sale_detailPD or btn_mso_wise_sale_detail or btn_mso_wise_sale_detailD or btn_dp_wise_sale_detail or btn_dp_wise_sale_detailD or btn_customer_nformation or btn_customer_nformationD or btn_customerProductS or btn_customerProductSD or btn_msowiseS or btn_msowiseSDLoad or btn_catMSOwiseS or btn_catDPwiseS or btn_catDPwiseSD or btn_productS or btn_productSD or btn_productSwithoutBonus or btn_productSwithoutBonusD or btn_customerProductSIncludinBonus or btn_customerProductSIncludinBonusD or btn_customerProductSExcludinBonus or btn_customerProductSExcludinBonusD or btn_dpwiseSD or btn_dpwiseSDD or btn_customerInvoiceProductS or btn_customerInvoiceProductSD or btn_customerInvoiceProductSwithBonus or btn_customerInvoiceProductSwithBonusD or btn_customerInvoiceProductSwithoutBonus or btn_customerInvoiceProductSwithoutBonusD or btn_productInvoicewiseSD or btn_productInvoicewiseSDwithBonus or btn_productInvoicewiseSDwithoutBonus or btn_productInvoicewiseSDD or btn_productInvoicewiseSDwithBonusD or btn_productInvoicewiseSDwithoutBonusD or btn_invoicewiseSD or btn_invoicewiseSDLoad or btn_summary or btn_causeofrtn or btn_causeofrtnDLoad or btn_DP_wise_sale_ss or btn_DP_wise_sale_ssD or btn_summaryD or btn_SalesClosingStockS or btn_SalesClosingStockSD or btn_SalesClosingStockSB or btn_SalesClosingStockSBD or btn_sComparision or btn_sComparisionD):
          
          date_from=request.vars.from_dt_2
          date_to=request.vars.to_dt_2
          
          depot=str(request.vars.sales_depot_id_sales)
          store=str(request.vars.store_id_sales)
          
          customer=str(request.vars.customer_id_sales)
          customerCat=str(request.vars.customer_category)
          customer_market=str(request.vars.customer_market)
          dman=str(request.vars.dman_id_sales)
          teritory=str(request.vars.t_id_sales)
          mso=str(request.vars.mso_id_sales)
          status=str(request.vars.status_sales)
          
          depot_id=depot
          store_id=store
          customer_id=customer
          dman_id=dman
          teritory=teritory
          mso_id=mso
          
          customerCat_id=customerCat
          
          depot_name=''
          store_name=''
          customer_name=''
          dman_name=''
          mso_name=''
          teritory_name=''
          customerCat_name=''
          dateFlag=True
          try:
              from_dt2=datetime.datetime.strptime(str(date_from),'%Y-%m-%d')
              to_dt2=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 

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
              if ((depot!='') & (depot.find('|') != -1)):             
                  depot_id=depot.split('|')[0].upper().strip()
                  depot_name=depot.split('|')[1].strip()
                  user_depot_address=''
                  if session.user_type!='Depot': 
                      depotRows = db((db.sm_depot.cid == session.cid) & (db.sm_depot.depot_id == depot_id)).select(db.sm_depot.name,db.sm_depot.depot_category,db.sm_depot.field1, limitby=(0, 1))
                      if depotRows:
                          user_depot_address=depotRows[0].field1         
                          session.user_depot_address=user_depot_address
#               return btn_summary
              if ((depot=='') | (store_id=='')) & (btn_summary==None) & (btn_summaryD==None) & (btn_sComparision==None) & (btn_sComparisionD==None):
                  session.flash="Required Branch and Store"
                  redirect(URL(c='report_sales',f='home')) 
                  
              else:
                  if ((store!='') & (store.find('|') != -1)) : 
                      store_id=store.split('|')[0].upper().strip()
                      store_name=store.split('|')[1].strip()
                  else:
                      store_id=store_id
                      store_name=''
                  if ((customer!='') & (customer.find('|') != -1)) :       
                      customer_id=customer.split('|')[0].upper().strip()
                      customer_name=customer.split('|')[1].strip()
                  else:
                      customer_id=customer_id
                      customer_name=''
                  
                  
                  if ((customerCat!='') & (customerCat.find('|') != -1)) :       
                      customerCat_id=customerCat.split('|')[0].upper().strip()
                      customerCat_name=customerCat.split('|')[1].strip()
                  else:
                      customerCat_id=customer_id
                      customerCat_name=''
                      
                  
                  if ((dman!='') & (dman.find('|') != -1)) :     
                      dman_id=dman.split('|')[0].upper().strip()
                      dman_name=dman.split('|')[1].strip()
                  else:
                      dman_id=dman_id
                      dman_name=''
                  
                  if ((teritory!='') & (teritory.find('|') != -1)) :    
                      teritory_id=teritory.split('|')[0].upper().strip()
                      teritory_name=teritory.split('|')[1].strip()
                  else:
                      teritory_id=teritory
                      teritory_name=''
                      
                  if ((mso!='') & (mso.find('|') != -1)) :    
                      mso_id=mso.split('|')[0].upper().strip()
                      mso_name=mso.split('|')[1].strip()
                  else:
                      mso_id=mso
                      mso_name=''
                  if ((customer_market!='') & (customer_market.find('|') != -1)) :    
                      market_id=customer_market.split('|')[0].upper().strip()
                      market_name=customer_market.split('|')[1].strip()
                  else:
                      market_id=customer_market
                      market_name=''   
                      
                      
        #          return btn_list_sales
                  if btn_list_sales:
                        redirect (URL('list_sales',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,dman_id=dman_id,dman_name=dman_name,mso_id=mso_id,mso_name=mso_name,status=status)))
                  if btn_customer_wise_sales:
                        redirect (URL('list_sales_customer_wise',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,dman_id=dman_id,dman_name=dman_name,mso_id=mso_id,mso_name=mso_name,status=status)))
                  if btn_item_wise_batch_sales:
                        redirect (URL('list_item_wise_batch_sales',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,dman_id=dman_id,dman_name=dman_name,mso_id=mso_id,mso_name=mso_name,status=status)))
                  if btn_item_wise_sales:
                        redirect (URL('list_item_wise_sales',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,dman_id=dman_id,dman_name=dman_name,mso_id=mso_id,mso_name=mso_name,status=status)))
                  if btn_list_oderdetail:
                        redirect (URL('list_oderdetail',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,mso_id=mso_id,mso_name=mso_name)))
                  if btn_list_oderdSummary_spowise:
                        redirect (URL('list_oderderSumRepWise',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,mso_id=mso_id,mso_name=mso_name)))
                  if btn_list_oderdSummary_spowiseDdate:
                        redirect (URL('list_oderderSumRepWiseDdate',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,mso_id=mso_id,mso_name=mso_name)))
    #               if btn_item_wise_sales_sheet:
    #                     redirect (URL('oderSheet',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,mso_id=mso_id,mso_name=mso_name)))
                  if btn_item_wise_sale_detail:
                        redirect (URL('itemWiseSalesSDetail',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  if btn_item_wise_sale_detailDLoad:
                        redirect (URL('itemWiseSalesSDetailDLoad',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                      
                  if btn_item_wise_sale_detail_land:
                        redirect (URL('itemWiseSalesSDetailLand',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,mso_id=mso_id,teritory_id=teritory_id,teritory_name=teritory_name,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  if btn_invoice_wise_sale_detail:
                        redirect (URL('invoiceWiseSalesSDetail',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,mso_id=mso_id,teritory_id=teritory_id,teritory_name=teritory_name,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  if btn_invoice_wise_sale_detailD:
                        redirect (URL('invoiceWiseSalesSDetailD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,mso_id=mso_id,teritory_id=teritory_id,teritory_name=teritory_name,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  
                  if btn_customer_wise_sale_detail:
                        redirect (URL('customerWiseSalesSDetail',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,mso_id=mso_id,teritory_id=teritory_id,teritory_name=teritory_name,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  if btn_customer_wise_sale_detailP:
                        redirect (URL('customerWiseSalesSDetailP',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,mso_id=mso_id,teritory_id=teritory_id,teritory_name=teritory_name,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  if btn_customer_wise_sale_detailPD:
                        redirect (URL('customerWiseSalesSDetailPD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,mso_id=mso_id,teritory_id=teritory_id,teritory_name=teritory_name,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  if btn_mso_wise_sale_detail:
                        redirect (URL('msoWiseSalesSDetail',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,mso_id=mso_id,teritory_id=teritory_id,teritory_name=teritory_name,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  if btn_mso_wise_sale_detailD:
                        redirect (URL('msoWiseSalesSDetailD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,mso_id=mso_id,teritory_id=teritory_id,teritory_name=teritory_name,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  
                  if btn_dp_wise_sale_detail:
                        redirect (URL('dpWiseSalesSDetail',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,mso_id=mso_id,teritory_id=teritory_id,teritory_name=teritory_name,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  if btn_dp_wise_sale_detailD:
                        redirect (URL('dpWiseSalesSDetailD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,mso_id=mso_id,teritory_id=teritory_id,teritory_name=teritory_name,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  
                  if btn_customer_nformation:
                        redirect (URL('customrInformation',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  if btn_customer_nformationD:
                        redirect (URL('customrInformationDownload',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name)))
                  
                  if btn_msowiseS:  
                        redirect (URL('msowiseS',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  if btn_msowiseSDLoad:  
                        redirect (URL('msowiseSDLoad',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  if btn_catMSOwiseS:
                        redirect (URL('catMSOwiseS',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,customerCat_id=customerCat_id, customerCat_name=customerCat_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name)))
                  if btn_catDPwiseS:
                        redirect (URL('catDPwiseS',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,customerCat_id=customerCat_id, customerCat_name=customerCat_name, dman_id=dman_id,dman_name=dman_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name)))
                  if btn_catDPwiseSD:
                        redirect (URL('catDPwiseSD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,customerCat_id=customerCat_id, customerCat_name=customerCat_name, dman_id=dman_id,dman_name=dman_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  if btn_dpwiseSD:
                       redirect (URL('dpwiseSD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,customerCat_id=customerCat_id, customerCat_name=customerCat_name, dman_id=dman_id,dman_name=dman_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  if btn_dpwiseSDD:
                       redirect (URL('dpwiseSDD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,customerCat_id=customerCat_id, customerCat_name=customerCat_name, dman_id=dman_id,dman_name=dman_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))        
                  if btn_customerProductS:
                        redirect (URL('customrProductwiseS',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  if btn_customerProductSD:
                        redirect (URL('customrProductwiseSD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))      
                  if btn_productS:
                      redirect (URL('productwiseS',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  if btn_productSD:
                      redirect (URL('productwiseSD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  if btn_productSwithoutBonus:
                      redirect (URL('productwiseSwithoutBonus',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  if btn_productSwithoutBonusD:
                      redirect (URL('productwiseSwithoutBonusD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  if btn_customerProductSIncludinBonus:
                        redirect (URL('customrProductwiseSIncludingBonus',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  if btn_customerProductSIncludinBonusD:
                        redirect (URL('customrProductwiseSIncludingBonusD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  if btn_customerProductSExcludinBonus:
                       redirect (URL('customrProductwiseSExcludingBonus',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  if btn_customerProductSExcludinBonusD:
                       redirect (URL('customrProductwiseSExcludingBonusD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                          
                  if btn_customerInvoiceProductS:
                       redirect (URL('customrInvoiceProductwiseS',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  if btn_customerInvoiceProductSD:
                       redirect (URL('customrInvoiceProductwiseSD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  if btn_customerInvoiceProductSwithBonus:
                        redirect (URL('customrInvoiceProductwiseSwithBonus',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  if btn_customerInvoiceProductSwithBonusD:
                        redirect (URL('customrInvoiceProductwiseSwithBonusD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  if btn_customerInvoiceProductSwithoutBonus:
                        redirect (URL('customrInvoiceProductwiseSwithoutBonus',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  if btn_customerInvoiceProductSwithoutBonusD:
                        redirect (URL('customrInvoiceProductwiseSwithoutBonusD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  if btn_productInvoicewiseSD:
                        redirect (URL('productInvoicewiseSD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  if btn_productInvoicewiseSDD:
                        redirect (URL('productInvoicewiseSDD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))        
                  if btn_productInvoicewiseSDwithBonus:
                        redirect (URL('productInvoicewiseSDwithBonus',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  if btn_productInvoicewiseSDwithBonusD:
                        redirect (URL('productInvoicewiseSDwithBonusD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  
                  if btn_productInvoicewiseSDwithoutBonus:
                        redirect (URL('productInvoicewiseSDwithoutBonus',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  
                  
                          
                  
                  if btn_productInvoicewiseSDwithoutBonusD:
                        redirect (URL('productInvoicewiseSDwithoutBonusD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  
                  
                  if btn_summary:
                        redirect (URL('summaryReport',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  if btn_summaryD:
                        redirect (URL('summaryReportD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                                                  
                  if btn_invoicewiseSD:
                        redirect (URL('invoicewiseSD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  if btn_invoicewiseSDLoad:
                        redirect (URL('invoicewiseSDLoad',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                                                        
                  if btn_causeofrtn:
                        redirect (URL('causeofRet',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  if btn_causeofrtnDLoad:
                        redirect (URL('causeofRetD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                                            
                  if btn_DP_wise_sale_ss:
                        redirect (URL('dp_wise_sale_ss',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,dman_id=dman_id,dman_name=dman_name,market_id=market_id,market_name=market_name)))
                  if btn_DP_wise_sale_ssD:
                        redirect (URL('dp_wise_sale_ssD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,dman_id=dman_id,dman_name=dman_name,market_id=market_id,market_name=market_name)))
                  if btn_SalesClosingStockS:   
                        redirect (URL('salesClosingStockS',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,dman_id=dman_id,dman_name=dman_name,market_id=market_id,market_name=market_name)))
                  if btn_SalesClosingStockSD:   
                        redirect (URL('salesClosingStockSD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,dman_id=dman_id,dman_name=dman_name,market_id=market_id,market_name=market_name)))  
                  if btn_SalesClosingStockSB:   
                        redirect (URL('salesClosingStockSB',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,dman_id=dman_id,dman_name=dman_name,market_id=market_id,market_name=market_name)))
                  if btn_SalesClosingStockSBD:   
                        redirect (URL('salesClosingStockSBD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,dman_id=dman_id,dman_name=dman_name,market_id=market_id,market_name=market_name)))
                  if btn_sComparision:
                        redirect (URL('msoSCTop',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,dman_id=dman_id,dman_name=dman_name,market_id=market_id,market_name=market_name)))
                  if btn_sComparisionD:
                        redirect (URL('msoSCTopD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,dman_id=dman_id,dman_name=dman_name,market_id=market_id,market_name=market_name)))
                        
                        
                  
         #     ================================================Sales End Nadira==========================================================================================                     
    if (btn_salesComparisionNational or btn_salesComparisionRsm or btn_salesComparisionFm or btn_salesComparisionTr or btn_salesComparisionTrDetail  or btn_salesComparisionNationalD or btn_salesComparisionRsmD or btn_salesComparisionFmD or btn_salesComparisionTrD or btn_salesComparisionTrDetail or btn_salesComparisionTrDetailD or btn_salesComparisionFmDetail or btn_salesComparisionFmDetailD or btn_salesComparisionRsmDetail or btn_salesComparisionRsmDetailD or btn_salesComparisionMarketDetail):
          date_from=request.vars.from_dt_3
          date_to=request.vars.to_dt_3

          depot=str(request.vars.sales_depot_id_SC)
          store=str(request.vars.store_id_SC)
          
          rsm_SC=str(request.vars.rsm_SC)
          fm_SC=str(request.vars.fm_SC)
          tr_SC=str(request.vars.tr_SC)

          depot_id=depot
          store_id=store

          depot_name=''
          store_name=''
          
          dateFlag=True
#           return 'asfsaf'
          try:
              from_dt2=datetime.datetime.strptime(str(date_from),'%Y-%m-%d')
          except:
              dateFlag=False
          
          
          if ((depot!='') & (depot.find('|') != -1)):             
              depot_id=depot.split('|')[0].upper().strip()
              depot_name=depot.split('|')[1].strip()
              
          else:
              depot_id=depot
              depot_name=''
          
          if ((store!='') & (store.find('|') != -1)) : 
              store_id=store.split('|')[0].upper().strip()
              store_name=store.split('|')[1].strip()
          else:
              store_id=store_id
              store_name=''
              
          if ((rsm_SC!='') & (store.find('|') != -1)) : 
              rsm_id=rsm_SC.split('|')[0].upper().strip()
              rsm_name=store.split('|')[1].strip()
          else:
              rsm_id=rsm_SC
              rsm_name=''
          if ((fm_SC!='') & (fm_SC.find('|') != -1)) : 
              fm_id=fm_SC.split('|')[0].upper().strip()
              fm_name=fm_SC.split('|')[1].strip()
          else:
              fm_id=fm_SC
              fm_name=''
          if ((tr_SC!='') & (tr_SC.find('|') != -1)) : 
              tr_id=tr_SC.split('|')[0].upper().strip()
              tr_name=tr_SC.split('|')[1].strip()
          else:
              tr_id=tr_SC
              tr_name=''
          if ((depot!='') & (depot.find('|') != -1)):             
                  depot_id=depot.split('|')[0].upper().strip()
                  depot_name=depot.split('|')[1].strip()
                  user_depot_address=''
                  if session.user_type!='Depot': 
                      depotRows = db((db.sm_depot.cid == session.cid) & (db.sm_depot.depot_id == depot_id)).select(db.sm_depot.name,db.sm_depot.depot_category,db.sm_depot.field1, limitby=(0, 1))
                      if depotRows:
                          user_depot_address=depotRows[0].field1         
                          session.user_depot_address=user_depot_address
                          
          if dateFlag==False:
              response.flash="Invalid Date "
          if btn_salesComparisionNational:
              redirect (URL('scNational',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name)))
          if btn_salesComparisionRsm:
              redirect (URL('scRsm',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name)))
          if btn_salesComparisionFm:
              redirect (URL('scFm',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name)))
          if btn_salesComparisionTr:
              redirect (URL('scTr',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name)))
          if btn_salesComparisionNationalD:
              redirect (URL('scNationalD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name)))
          if btn_salesComparisionRsmD:
              redirect (URL('scRsmD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name)))
          if btn_salesComparisionFmD:
              redirect (URL('scFmD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name)))
          if btn_salesComparisionTrD:
              redirect (URL('scTrD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name)))
          if btn_salesComparisionTrDetail: 
              redirect (URL('scTrDetail',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name)))       
          if btn_salesComparisionFmDetail: 
              redirect (URL('scFmDetail',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name)))       
          if btn_salesComparisionRsmDetail:
              redirect (URL('scRsmDetail',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name)))          
          if btn_salesComparisionTrDetailD: 
              redirect (URL('scTrDetailD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name)))       
          if btn_salesComparisionFmDetailD: 
              redirect (URL('scFmDetailD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name)))       
          if btn_salesComparisionRsmDetailD:
              redirect (URL('scRsmDetailD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name)))
          if btn_salesComparisionMarketDetail:
              redirect (URL('scMarketDetail',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name)))
          
          
          
                                                               
    if (btn_list_sales or btn_customer_wise_sales or btn_item_wise_batch_sales or btn_item_wise_sales or btn_list_oderdetail or btn_list_oderdSummary_spowise or btn_item_wise_sale_detail or btn_item_wise_sales_sheet):
          date_from=request.vars.to_dt
          date_to=request.vars.to_dt_2
          
          sl_from=request.vars.sales_sl_from
          sl_to=request.vars.sales_sl_to
          
          depot=str(request.vars.sales_depot_id_order)
          store=str(request.vars.store_id_order)
          
          customer=str(request.vars.customer_id_order)
          teritory=str(request.vars.t_id_order)
          mso=str(request.vars.mso_id_order)
          
          RadioGroupCheck=str(request.vars.RadioGroupCheck)
#           return RadioGroupCheck
          
          depot_id=depot
          store_id=store
          customer_id=customer
          teritory_id=teritory
          mso_id=mso
          
          depot_name=''
          store_name=''
          customer_name=''
          teritory_name=''
          mso_name=''
          dateFlag=True
#           return 'asfsaf'
          try:
              from_dt2=datetime.datetime.strptime(str(date_from),'%Y-%m-%d')
          except:
              dateFlag=False
          
#           return btn_item_wise_sales_sheet
          if ((depot!='') & (depot.find('|') != -1)):             
              depot_id=depot.split('|')[0].upper().strip()
              depot_name=depot.split('|')[1].strip()
              
          else:
              depot_id=depot
              depot_name=''
          
          if ((store!='') & (store.find('|') != -1)) : 
              store_id=store.split('|')[0].upper().strip()
              store_name=store.split('|')[1].strip()
          else:
              store_id=store_id
              store_name=''
          if ((customer!='') & (customer.find('|') != -1)) :       
              customer_id=customer.split('|')[0].upper().strip()
              customer_name=customer.split('|')[1].strip()
          else:
              customer_id=customer_id
              customer_name=''
          
          if ((teritory!='') & (teritory.find('|') != -1)) :     
              teritory_id=teritory.split('|')[0].upper().strip()
              teritory_name=teritory.split('|')[1].strip()
          else:
              teritory_id=teritory_id
              teritory_name=''
          if ((mso!='') & (mso.find('|') != -1)) :    
              mso_id=mso.split('|')[0].upper().strip()
              mso_name=mso.split('|')[1].strip()
          else:
              mso_id=mso_id
              mso_name=''
          
          if dateFlag==False:
              response.flash="Invalid Date "
          elif (teritory_id=='' and  mso_id=='' and customer_id=='' and btn_item_wise_sales_sheet!='Order Sheet' ):
              response.flash="Please select Teritory or Mso or Customer"
          else:              
              
    #          return btn_list_sales
              
              if btn_item_wise_sales_sheet:
                    redirect (URL('oderSheet',vars=dict(date_from=date_from,date_to=date_to,sl_from=sl_from,sl_to=sl_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,RadioGroupCheck=RadioGroupCheck)))  
         #     ================================================Sales End Nadira==========================================================================================                     
    
                          
    
    return dict(search_form=search_form)







#===================================================Sales Start Nadira=====================
def order():
    c_id=session.cid
    
    response.title='Sales-Invoice Wise'
    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    dman_id=str(request.vars.dman_id).strip()
    dman_name=str(request.vars.dman_name).strip()
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    status=str(request.vars.status).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)
    
    
#    return status
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
    qset=qset(db.sm_invoice_head.invoice_media!='OPENING')
    qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    qset_sum=db()
    qset_sum=qset_sum(db.sm_invoice_head.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice_head.invoice_media!='OPENING')
    qset_sum=qset_sum((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    if (depot_id!=''):
        qset=qset(db.sm_invoice_head.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice_head.store_id==store_id)
        qset_sum=qset_sum(db.sm_invoice_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_invoice_head.client_id==customer_id)
        qset_sum=qset_sum(db.sm_invoice_head.client_id==customer_id)
    if (dman_id!=''):
        qset=qset(db.sm_invoice_head.d_man_id==dman_id)
        qset_sum=qset_sum(db.sm_invoice_head.d_man_id==dman_id)
    if (mso_id!=''):
        qset=qset(db.sm_invoice_head.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_invoice_head.rep_id==mso_id)
        
    if (mso_id!=''):
        qset=qset(db.sm_invoice_head.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_invoice_head.rep_id==mso_id)
    if (status!=''):
        if (status=='Invoiced'):
            qset=qset(db.sm_invoice_head.status==status)
            qset_sum=qset_sum(db.sm_invoice_head.status==status)
        else:
            qset=qset((db.sm_invoice_head.status!='Invoiced') & (db.sm_invoice_head.status!='Cancelled'))
            qset_sum=qset_sum((db.sm_invoice_head.status!='Invoiced') & (db.sm_invoice_head.status!='Cancelled'))
   
    
    
    records=qset.select(db.sm_invoice_head.ALL,orderby=db.sm_invoice_head.depot_id|db.sm_invoice_head.store_id|db.sm_invoice_head.sl,limitby=limitby)
    record_sum=qset.select(db.sm_invoice_head.total_amount.sum(),((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat)-db.sm_invoice_head.return_discount).sum()  )
#     return record_sum
    net_amount=0.0
    net_return=0.0

    net_return=0.0
    for rec in record_sum:
        net_amount=rec[db.sm_invoice_head.total_amount.sum()]
        net_return=rec[(((db.sm_invoice_head.return_tp + db.sm_invoice_head.return_vat) - db.sm_invoice_head.return_discount)).sum()]
        if net_amount==None:
            net_amount=0.0
        if net_return==None:
            net_return=0.0
    
#     net_return=((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat)-db.sm_invoice_head.return_discount)
    
    return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name, dman_id=dman_id,dman_name=dman_name, mso_id=mso_id, mso_name=mso_name,status=status,net_amount=net_amount,net_return=net_return,page=page,items_per_page=items_per_page)    

def list_sales():
    c_id=session.cid
    
    response.title='Sales-Invoice Wise'
    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    dman_id=str(request.vars.dman_id).strip()
    dman_name=str(request.vars.dman_name).strip()
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    status=str(request.vars.status).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)
    
#    return status
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
    qset=qset(db.sm_invoice_head.invoice_media!='OPENING')
    qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    qset_sum=db()
    qset_sum=qset_sum(db.sm_invoice_head.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice_head.invoice_media!='OPENING')
    qset_sum=qset_sum((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    if (depot_id!=''):
        qset=qset(db.sm_invoice_head.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice_head.store_id==store_id)
        qset_sum=qset_sum(db.sm_invoice_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_invoice_head.client_id==customer_id)
        qset_sum=qset_sum(db.sm_invoice_head.client_id==customer_id)
    if (dman_id!=''):
        qset=qset(db.sm_invoice_head.d_man_id==dman_id)
        qset_sum=qset_sum(db.sm_invoice_head.d_man_id==dman_id)
    if (mso_id!=''):
        qset=qset(db.sm_invoice_head.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_invoice_head.rep_id==mso_id)
        
    if (mso_id!=''):
        qset=qset(db.sm_invoice_head.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_invoice_head.rep_id==mso_id)
    if (status!=''):
        if (status=='Invoiced'):
            qset=qset(db.sm_invoice_head.status==status)
            qset_sum=qset_sum(db.sm_invoice_head.status==status)
        else:
            qset=qset((db.sm_invoice_head.status!='Invoiced') & (db.sm_invoice_head.status!='Cancelled'))
            qset_sum=qset_sum((db.sm_invoice_head.status!='Invoiced') & (db.sm_invoice_head.status!='Cancelled'))
   
    
    
    records=qset.select(db.sm_invoice_head.ALL,orderby=db.sm_invoice_head.depot_id|db.sm_invoice_head.store_id|db.sm_invoice_head.sl,limitby=limitby)
    record_sum=qset.select(db.sm_invoice_head.total_amount.sum(),((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat)-db.sm_invoice_head.return_discount).sum()  )
#     return record_sum
    net_amount=0.0
    net_return=0.0

    net_return=0.0
    for rec in record_sum:
        net_amount=rec[db.sm_invoice_head.total_amount.sum()]
        net_return=rec[(((db.sm_invoice_head.return_tp + db.sm_invoice_head.return_vat) - db.sm_invoice_head.return_discount)).sum()]
        if net_amount==None:
            net_amount=0.0
        if net_return==None:
            net_return=0.0
    
#     net_return=((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat)-db.sm_invoice_head.return_discount)
    
    return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name, dman_id=dman_id,dman_name=dman_name, mso_id=mso_id, mso_name=mso_name,status=status,net_amount=net_amount,net_return=net_return,page=page,items_per_page=items_per_page)    


def list_sales_customer_wise():
    c_id=session.cid
    
    response.title='Sales-Customer Wise'
    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    dman_id=str(request.vars.dman_id).strip()
    dman_name=str(request.vars.dman_name).strip()
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    status=str(request.vars.status).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)
    
    
    #    return status
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
    qset=qset(db.sm_invoice_head.invoice_media!='OPENING')
    qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    qset_sum=db()
    qset_sum=qset_sum(db.sm_invoice_head.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice_head.invoice_media!='OPENING')
    qset_sum=qset_sum((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    if (depot_id!=''):
        qset=qset(db.sm_invoice_head.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice_head.store_id==store_id)
        qset_sum=qset_sum(db.sm_invoice_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_invoice_head.client_id==customer_id)
        qset_sum=qset_sum(db.sm_invoice_head.client_id==customer_id)
    if (dman_id!=''):
        qset=qset(db.sm_invoice_head.d_man_id==dman_id)
        qset_sum=qset_sum(db.sm_invoice_head.d_man_id==dman_id)
    if (mso_id!=''):
        qset=qset(db.sm_invoice_head.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_invoice_head.rep_id==mso_id)
        
    if (mso_id!=''):
        qset=qset(db.sm_invoice_head.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_invoice_head.rep_id==mso_id)
    if (status!=''):
        if (status=='Invoiced'):
            qset=qset(db.sm_invoice_head.status==status)
            qset_sum=qset_sum(db.sm_invoice_head.status==status)
        else:
            qset=qset((db.sm_invoice_head.status!='Invoiced') & (db.sm_invoice_head.status!='Cancelled'))
            qset_sum=qset_sum((db.sm_invoice_head.status!='Invoiced') & (db.sm_invoice_head.status!='Cancelled'))
    
    
    
    records=qset.select(db.sm_invoice_head.client_id,db.sm_invoice_head.client_name,db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),  groupby=db.sm_invoice_head.client_id,orderby=db.sm_invoice_head.depot_id|db.sm_invoice_head.store_id|db.sm_invoice_head.sl,limitby=limitby)
#     return records
    record_sum=qset_sum.select(db.sm_invoice_head.total_amount.sum(),((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat)-db.sm_invoice_head.return_discount).sum()  )
#     return record_sum
    net_amount=0.0
    net_return=0.0
    
    net_return=0.0
    for rec in record_sum:
        net_amount=rec[db.sm_invoice_head.total_amount.sum()]
        net_return=rec[(((db.sm_invoice_head.return_tp + db.sm_invoice_head.return_vat) - db.sm_invoice_head.return_discount)).sum()]
        if net_amount==None:
            net_amount=0.0
        if net_return==None:
            net_return=0.0
    #     net_return=((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat)-db.sm_invoice_head.return_discount)
    
    return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name, dman_id=dman_id,dman_name=dman_name, mso_id=mso_id, mso_name=mso_name,status=status,net_amount=net_amount,net_return=net_return,page=page,items_per_page=items_per_page)    


def list_item_wise_batch_sales():
    c_id=session.cid
    
    response.title='Sales-Customer Wise'
    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    dman_id=str(request.vars.dman_id).strip()
    dman_name=str(request.vars.dman_name).strip()
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    status=str(request.vars.status).strip()
    
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)
     
    
    #    return status
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    qset=db()
    qset=qset(db.sm_invoice.cid==c_id)
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.invoice_media!='OPENING')
    qset=qset(db.sm_invoice_head.sl==db.sm_invoice.sl)
    qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    qset_sum=db()
    qset_sum=qset_sum(db.sm_invoice.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice_head.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice_head.invoice_media!='OPENING')
    qset_sum=qset_sum(db.sm_invoice_head.sl==db.sm_invoice.sl)
    qset_sum=qset_sum((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    if (depot_id!=''):
        qset=qset(db.sm_invoice.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_invoice.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice.store_id==store_id)
        qset_sum=qset_sum(db.sm_invoice.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_invoice.client_id==customer_id)
        qset_sum=qset_sum(db.sm_invoice.client_id==customer_id)
    if (dman_id!=''):
        qset=qset(db.sm_invoice.d_man_id==dman_id)
        qset_sum=qset_sum(db.sm_invoice.d_man_id==dman_id)
    if (mso_id!=''):
        qset=qset(db.sm_invoice.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_invoice.rep_id==mso_id)
        
    if (mso_id!=''):
        qset=qset(db.sm_invoice.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_invoice.rep_id==mso_id)
    if (status!=''):
        if (status=='Invoiced'):
            qset=qset(db.sm_invoice.status==status)
            qset_sum=qset_sum(db.sm_invoice.status==status)
        else:
            qset=qset((db.sm_invoice.status!='Invoiced') & (db.sm_invoice.status!='Cancelled'))
            qset_sum=qset_sum((db.sm_invoice.status!='Invoiced') & (db.sm_invoice.status!='Cancelled'))
    
    
    
    records=qset.select(db.sm_invoice.item_id,db.sm_invoice.item_name,db.sm_invoice.batch_id,db.sm_invoice.quantity.sum(),db.sm_invoice.bonus_qty.sum(),db.sm_invoice.price,db.sm_invoice.discount,db.sm_invoice.item_vat,db.sm_invoice.item_vat.sum(),db.sm_invoice.return_qty.sum(),db.sm_invoice.return_bonus_qty.sum(),db.sm_invoice.return_rate,  groupby=db.sm_invoice.item_id | db.sm_invoice.batch_id,orderby=db.sm_invoice.item_name|db.sm_invoice.batch_id,limitby=limitby)
#     return records
    record_sum=qset_sum.select(((db.sm_invoice.price+db.sm_invoice.item_vat) * db.sm_invoice.quantity+db.sm_invoice.discount).sum(),(db.sm_invoice.return_qty * db.sm_invoice.return_rate).sum()  )
#     return db._lastsql
    net_amount=0.0
    net_return=0.0
    
    net_return=0.0
    for rec in record_sum:
        net_amount=rec[((db.sm_invoice.price+db.sm_invoice.item_vat) * db.sm_invoice.quantity+db.sm_invoice.discount).sum()]
        net_return=rec[(db.sm_invoice.return_qty * db.sm_invoice.return_rate).sum()]
        if net_amount==None:
            net_amount=0.0
        if net_return==None:
            net_return=0.0
    
    #     net_return=((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat)-db.sm_invoice_head.return_discount)
    
    return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name, dman_id=dman_id,dman_name=dman_name, mso_id=mso_id, mso_name=mso_name,status=status,net_amount=net_amount,net_return=net_return,page=page,items_per_page=items_per_page)    

    
def list_item_wise_sales():
    c_id=session.cid
    
    response.title='Sales-Customer Wise'
    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    dman_id=str(request.vars.dman_id).strip()
    dman_name=str(request.vars.dman_name).strip()
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    status=str(request.vars.status).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)
    
    
    #    return status
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    qset=db()
    qset=qset(db.sm_invoice.cid==c_id)
    qset=qset(db.sm_invoice_head.cid==c_id)
#     qset=qset(db.sm_invoice_head.invoice_media!='OPENING')
    qset=qset(db.sm_invoice_head.sl==db.sm_invoice.sl)
    qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    qset_sum=db()
    qset_sum=qset_sum(db.sm_invoice.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice_head.cid==c_id)
#     qset_sum=qset_sum(db.sm_invoice_head.invoice_media!='OPENING')
    qset_sum=qset_sum(db.sm_invoice_head.sl==db.sm_invoice.sl)
    qset_sum=qset_sum((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    if (depot_id!=''):
        qset=qset(db.sm_invoice.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_invoice.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice.store_id==store_id)
        qset_sum=qset_sum(db.sm_invoice.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_invoice.client_id==customer_id)
        qset_sum=qset_sum(db.sm_invoice.client_id==customer_id)
    if (dman_id!=''):
        qset=qset(db.sm_invoice.d_man_id==dman_id)
        qset_sum=qset_sum(db.sm_invoice.d_man_id==dman_id)
    if (mso_id!=''):
        qset=qset(db.sm_invoice.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_invoice.rep_id==mso_id)
        
    if (mso_id!=''):
        qset=qset(db.sm_invoice.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_invoice.rep_id==mso_id)
    if (status!=''):
        if (status=='Invoiced'):
            qset=qset(db.sm_invoice.status==status)
            qset_sum=qset_sum(db.sm_invoice.status==status)
        else:
            qset=qset((db.sm_invoice.status!='Invoiced') & (db.sm_invoice.status!='Cancelled'))
            qset_sum=qset_sum((db.sm_invoice.status!='Invoiced') & (db.sm_invoice.status!='Cancelled'))
    
    
    
    records=qset.select(db.sm_invoice.item_id,db.sm_invoice.item_name,db.sm_invoice.batch_id,db.sm_invoice.quantity.sum(),db.sm_invoice.bonus_qty.sum(),db.sm_invoice.price,db.sm_invoice.item_vat.sum(),db.sm_invoice.return_qty.sum(),db.sm_invoice.return_bonus_qty.sum(),db.sm_invoice.return_rate,  groupby=db.sm_invoice.item_id,orderby=db.sm_invoice.item_name,limitby=limitby)
#     return records
    record_sum=qset_sum.select(((db.sm_invoice.price+db.sm_invoice.item_vat) * db.sm_invoice.quantity+db.sm_invoice.discount).sum(),(db.sm_invoice.return_qty * db.sm_invoice.return_rate).sum()  )
#     return record_sum
    net_amount=0.0
    net_return=0.0
    
    net_return=0.0
    for rec in record_sum:
        net_amount=rec[((db.sm_invoice.price+db.sm_invoice.item_vat) * db.sm_invoice.quantity+db.sm_invoice.discount).sum()]
        net_return=rec[(db.sm_invoice.return_qty * db.sm_invoice.return_rate).sum()]
    
    #     net_return=((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat)-db.sm_invoice_head.return_discount)
    
    return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name, dman_id=dman_id,dman_name=dman_name, mso_id=mso_id, mso_name=mso_name,status=status,net_amount=net_amount,net_return=net_return,page=page,items_per_page=items_per_page)    





# Nadira
#=====================================Order detail==============================================

def list_oderdetail():
    c_id=session.cid
    
    response.title='Order Detail'
    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    qset=db()
    qset=qset(db.sm_order.cid==c_id)

    qset=qset((db.sm_order.order_date >= date_from) & (db.sm_order.order_date < date_to_m))
    
    qset_sum=db()
    qset_sum=qset_sum(db.sm_order.cid==c_id)
    
    qset_sum=qset_sum((db.sm_order.order_date >= date_from) & (db.sm_order.order_date < date_to_m))
    
    if (depot_id!=''):
        qset=qset(db.sm_order.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_order.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_order.store_id==store_id)
        qset_sum=qset_sum(db.sm_order.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_order.client_id==customer_id)
        qset_sum=qset_sum(db.sm_order.client_id==customer_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_order.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_order.rep_id==mso_id)
        
  
    records=qset.select(db.sm_order.ALL,orderby=db.sm_order.depot_id|db.sm_order.store_id|db.sm_order.sl,limitby=limitby)
#     return db._lastsql
    record_sum=qset.select((db.sm_order.price* db.sm_order.quantity).sum())

    total=0.0
    
    for rec in record_sum:
        total=rec[(db.sm_order.price* db.sm_order.quantity).sum()]
    
#     net_return=((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat)-db.sm_invoice_head.return_discount)
    
    return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  mso_id=mso_id, mso_name=mso_name,total=total,page=page,items_per_page=items_per_page)    
 #=====================================Order detail Download==============================================

def downloadorderDetail():
    c_id=session.cid
    
#     response.title='Sales-Invoice Wise'
    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
   
    
    qset=db()
    qset=qset(db.sm_order.cid==c_id)

    qset=qset((db.sm_order.order_date >= date_from) & (db.sm_order.order_date < date_to_m))
    
    qset_sum=db()
    qset_sum=qset_sum(db.sm_order.cid==c_id)

    qset_sum=qset_sum((db.sm_order.order_date >= date_from) & (db.sm_order.order_date < date_to_m))
    if (depot_id!=''):
        qset=qset(db.sm_order.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_order.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_order.store_id==store_id)
        qset_sum=qset_sum(db.sm_order.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_order.client_id==customer_id)
        qset_sum=qset_sum(db.sm_order.client_id==customer_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_order.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_order.rep_id==mso_id)
        
  
    records=qset.select(db.sm_order.ALL,orderby=db.sm_order.depot_id|db.sm_order.store_id|db.sm_order.sl)
#     return db._lastsql
    record_sum=qset.select((db.sm_order.price* db.sm_order.quantity).sum())

    total=0.0
    
    for rec in record_sum:
        total=rec[(db.sm_order.price* db.sm_order.quantity).sum()]
    
 
    
    
    #REmove , from record.Cause , means new column in excel    
    myString='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='Store,'+store_id+'|'+store_name+'\n'
    myString+='Customer,'+customer_id+'|'+customer_name+'\n'
    myString+='MSO,'+mso_id+'|'+mso_name+'\n\n'
    
    myString=myString+'Total,'+str(total)+'\n\n\n'
        
    myString+='SL,Region,Region Name,Area,Area Name,Territory,Territory Name,MSO,MSOName,Customer ID,Customer Name,Item ID,Item Name,Qty,Rate,Total\n'
    
    
    for rec in records:
        sl=rec.sl
        region=rec.level2_id
        rigion_name=rec.level2_name
        area=rec.level1_id
        area_name=rec.level1_name
        teritory=rec.area_id
        teritory_name=rec.area_name
        rep_id=rec.rep_id
        rep_name=rec.rep_name
        client_id=rec.client_id
        client_name=rec.client_name
        item=rec.item_id
        item_name=rec.item_name
        qty=rec.quantity
        price=rec.price
        total_amn=float(price)*float(qty)
        
        

         
               
        myString+=str(sl)+','+str(region)+','+str(rigion_name)+','+str(area)+','+str(area_name)+','+str(teritory)+','+str(teritory_name)+','+str(rep_id)+','+str(rep_name)+','+str(client_id)+','+str(client_name)+','+str(item)+','+str(item_name)+','+str(qty)+','+str(price)+','+str(total_amn)+'\n'
         
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_order_detail.csv'   
    return str(myString) 

#=====================================list_oderderSumRepWise==============================================

def list_oderderSumRepWise():
    c_id=session.cid
    
    response.title='Order Count MSO Wise'
    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    qset=db()
    qset=qset(db.sm_order_head.cid==c_id)

    qset=qset((db.sm_order_head.order_date >= date_from) & (db.sm_order_head.order_date < date_to_m))
    
    qset_sum=db()
    qset_sum=qset_sum(db.sm_order_head.cid==c_id)

    qset_sum=qset_sum((db.sm_order_head.order_date >= date_from) & (db.sm_order_head.order_date < date_to_m))
    if (depot_id!=''):
        qset=qset(db.sm_order_head.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_order_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_order_head.store_id==store_id)
        qset_sum=qset_sum(db.sm_order_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_order_head.client_id==customer_id)
        qset_sum=qset_sum(db.sm_order_head.client_id==customer_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_order_head.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_order_head.rep_id==mso_id)
        
  
    records=qset.select(db.sm_order_head.ALL,db.sm_order_head.sl.count(),orderby=db.sm_order_head.rep_id | |db.sm_order_head.area_id,groupby=db.sm_order_head.rep_id||db.sm_order_head.area_id ,limitby=limitby)
#     return db._lastsql
    record_sum=qset.select(db.sm_order_head.sl.count())
#     return records
    total=0.0
    
    for rec in record_sum:
        total=rec[db.sm_order_head.sl.count()]
    
#     net_return=((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat)-db.sm_invoice_head.return_discount)
    
    return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  mso_id=mso_id, mso_name=mso_name,total=total,page=page,items_per_page=items_per_page)    

def list_oderderSumRepWiseDdate():
    c_id=session.cid
    
    response.title='Order Count MSO Wise'
    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    qset=db()
    qset=qset(db.sm_order_head.cid==c_id)

    qset=qset((db.sm_order_head.delivery_date >= date_from) & (db.sm_order_head.delivery_date < date_to_m))
    
    qset_sum=db()
    qset_sum=qset_sum(db.sm_order_head.cid==c_id)

    qset_sum=qset_sum((db.sm_order_head.delivery_date >= date_from) & (db.sm_order_head.delivery_date < date_to_m))
    if (depot_id!=''):
        qset=qset(db.sm_order_head.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_order_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_order_head.store_id==store_id)
        qset_sum=qset_sum(db.sm_order_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_order_head.client_id==customer_id)
        qset_sum=qset_sum(db.sm_order_head.client_id==customer_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_order_head.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_order_head.rep_id==mso_id)
        
  
    records=qset.select(db.sm_order_head.ALL,db.sm_order_head.sl.count(),orderby=db.sm_order_head.rep_id|db.sm_order_head.area_id,groupby=db.sm_order_head.rep_id|db.sm_order_head.area_id ,limitby=limitby)
#     return db._lastsql
    record_sum=qset.select(db.sm_order_head.sl.count())
#     return records
    total=0.0
    
    for rec in record_sum:
        total=rec[db.sm_order_head.sl.count()]
    
#     net_return=((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat)-db.sm_invoice_head.return_discount)
    
    return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  mso_id=mso_id, mso_name=mso_name,total=total,page=page,items_per_page=items_per_page)    
def list_oderderSumRepWiseDownloadDdate():
    c_id=session.cid
    
#     response.title='Sales-Invoice Wise'
    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
   
    
    qset=db()
    qset=qset(db.sm_order_head.cid==c_id)

    qset=qset((db.sm_order_head.delivery_date >= date_from) & (db.sm_order_head.delivery_date < date_to_m))
    
    qset_sum=db()
    qset_sum=qset_sum(db.sm_order_head.cid==c_id)
    
    qset_sum=qset_sum((db.sm_order_head.delivery_date >= date_from) & (db.sm_order_head.delivery_date < date_to_m))
    if (depot_id!=''):
        qset=qset(db.sm_order_head.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_order_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_order_head.store_id==store_id)
        qset_sum=qset_sum(db.sm_order_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_order_head.client_id==customer_id)
        qset_sum=qset_sum(db.sm_order_head.client_id==customer_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_order_head.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_order_head.rep_id==mso_id)
        
  
    records=qset.select(db.sm_order_head.ALL,db.sm_order_head.sl.count(),orderby=db.sm_order_head.rep_id|db.sm_order_head.area_id,groupby=db.sm_order_head.rep_id|db.sm_order_head.area_id )
#     return db._lastsql
    record_sum=qset.select(db.sm_order_head.sl.count())
#     return records
    total=0.0
    
    for rec in record_sum:
        total=rec[db.sm_order_head.sl.count()]
        
   #REmove , from record.Cause , means new column in excel    
    myString='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='Store,'+store_id+'|'+store_name+'\n'
    myString+='Customer,'+customer_id+'|'+customer_name+'\n'
    myString+='MSO,'+mso_id+'|'+mso_name+'\n\n'
    
    myString=myString+'Total,'+str(total)+'\n\n\n'
        
    myString+='MSO,Name,Territory,Territory Name,Total\n'
    
    
    for rec in records:
        rep_id=rec[db.sm_order_head.rep_id]
        rep_name=rec[db.sm_order_head.rep_name]
        teritory=rec[db.sm_order_head.area_id]
        teritory_name=rec[db.sm_order_head.area_name]
        
        total_o=rec[db.sm_order_head.sl.count()]
        
        

         
               
        myString+=str(rep_id)+','+str(rep_name)+','+str(teritory)+','+str(teritory_name)+','+str(total_o)+'\n'
         
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_orderCountRepWiswDelDate.csv'   
    return str(myString) 

def list_oderderSumRepWiseDownload():
    c_id=session.cid
    
#     response.title='Sales-Invoice Wise'
    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
   
    
    qset=db()
    qset=qset(db.sm_order_head.cid==c_id)

    qset=qset((db.sm_order_head.order_date >= date_from) & (db.sm_order_head.order_date < date_to_m))
    
    qset_sum=db()
    qset_sum=qset_sum(db.sm_order_head.cid==c_id)
    
    qset_sum=qset_sum((db.sm_order_head.order_date >= date_from) & (db.sm_order_head.order_date < date_to_m))
    if (depot_id!=''):
        qset=qset(db.sm_order_head.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_order_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_order_head.store_id==store_id)
        qset_sum=qset_sum(db.sm_order_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_order_head.client_id==customer_id)
        qset_sum=qset_sum(db.sm_order_head.client_id==customer_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_order_head.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_order_head.rep_id==mso_id)
        
  
    records=qset.select(db.sm_order_head.ALL,db.sm_order_head.sl.count(),orderby=db.sm_order_head.depot_id|db.sm_order_head.store_id|db.sm_order_head.rep_id|db.sm_order_head.area_id,groupby=db.sm_order_head.rep_id|db.sm_order_head.area_id )
#     return db._lastsql
    record_sum=qset.select(db.sm_order_head.sl.count())
#     return records
    total=0.0
    
    for rec in record_sum:
        total=rec[db.sm_order_head.sl.count()]
        
   #REmove , from record.Cause , means new column in excel    
    myString='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='Store,'+store_id+'|'+store_name+'\n'
    myString+='Customer,'+customer_id+'|'+customer_name+'\n'
    myString+='MSO,'+mso_id+'|'+mso_name+'\n\n'
    
    myString=myString+'Total,'+str(total)+'\n\n\n'
        
    myString+='MSO,Name,Territory,Territory Name,Total\n'
    
    
    for rec in records:
        rep_id=rec[db.sm_order_head.rep_id]
        rep_name=rec[db.sm_order_head.rep_name]
        teritory=rec[db.sm_order_head.area_id]
        teritory_name=rec[db.sm_order_head.area_name]
        
        total_o=rec[db.sm_order_head.sl.count()]
        
        

         
               
        myString+=str(rep_id)+','+str(rep_name)+','+str(teritory)+','+str(teritory_name)+','+str(total_o)+'\n'
         
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_orderCountRepWisw.csv'   
    return str(myString) 


def oderSheet():
    c_id=session.cid
    
    response.title='Order Sheet'
    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    
    sl_from=request.vars.sl_from
    sl_to=request.vars.sl_to
#     return  sl_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    RadioGroupCheck=str(request.vars.RadioGroupCheck).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)
    
    
    date_from_check=datetime.datetime.strptime(str(date_from),'%Y-%m-%d')
    date_to_check=datetime.datetime.strptime(str(date_to_m).split(' ')[0],'%Y-%m-%d') 
    
    
    dateDiff=(date_to_check-date_from_check).days
#     return dateDiff
    if int(dateDiff) > 7:
        session.flash="Maximum 7 days allowed between Date Range"
        redirect(URL(c='report_sales',f='home')) 
#     return dateDiff
    
#     return 'asdas'
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    qset=db()
    qset=qset(db.sm_order.cid==c_id)
    qset=qset(db.sm_client.cid==c_id)
    qset=qset(db.sm_client.client_id==db.sm_order.client_id)
    
    if RadioGroupCheck=='Order':
        qset=qset((db.sm_order.order_date >= date_from) & (db.sm_order.order_date < date_to_m))
    if RadioGroupCheck=='Delivery':
        qset=qset((db.sm_order.delivery_date >= date_from) & (db.sm_order.delivery_date < date_to_m))
    
    
    
    
    
#     qset_sum=db()
#     qset_sum=qset_sum(db.sm_order.cid==c_id)
#     if RadioGroupCheck=='Order':
#         qset_sum=qset_sum((db.sm_order.order_date >= date_from) & (db.sm_order.order_date < date_to_m))
#     if RadioGroupCheck=='Delivery':
#         qset_sum=qset_sum((db.sm_order.delivery_date >= date_from) & (db.sm_order.delivery_date < date_to_m))
    
    if (sl_from!=''):
        qset=qset(db.sm_order.sl>=sl_from)
#         qset_sum=qset_sum(db.sm_order.sl>=sl_from)
        
    if (sl_to!=''):    
        qset=qset(db.sm_order.sl<=sl_to)        
#         qset_sum=qset_sum(db.sm_order.sl<=sl_to)
    
    if (depot_id!=''):
        qset=qset(db.sm_order.depot_id==depot_id)
#         qset_sum=qset_sum(db.sm_order.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_order.store_id==store_id)
#         qset_sum=qset_sum(db.sm_order.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_order.client_id==customer_id)
#         qset_sum=qset_sum(db.sm_order.client_id==customer_id)
    
    if (teritory_id!=''):
        qset=qset(db.sm_order.area_id==teritory_id)
#         qset_sum=qset_sum(db.sm_order.area_id==teritory_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_order.rep_id==mso_id)
#         qset_sum=qset_sum(db.sm_order.rep_id==mso_id)
        
  
    records=qset.select(db.sm_order.ALL,db.sm_client.address,db.sm_client.market_id,db.sm_client.market_name,orderby=db.sm_order.depot_id|db.sm_order.store_id|db.sm_order.sl)
#     return db._lastsql
    if not records:
        session.flash="Order Not Available"
        redirect(URL(c='report_sales',f='home')) 
        
    
#     record_sum=qset.select((db.sm_order.price* db.sm_order.quantity).sum())

#     total=0.0
#     
#     for rec in record_sum:
#         total=rec[(db.sm_order.price* db.sm_order.quantity).sum()]
    
#     net_return=((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat)-db.sm_invoice_head.return_discount)
    
    return dict(records=records,date_from=date_from,sl_from=sl_from,sl_to=sl_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  mso_id=mso_id, mso_name=mso_name,page=page,items_per_page=items_per_page)    
 
 
 
def itemWiseSalesSDetail():
    c_id=session.cid
    response.title='Item Wise Sales Statement Detail'
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
   
    qset=db()
    qset=qset(db.sm_invoice.cid==c_id)
    qset=qset(db.sm_invoice.status=='Invoiced')
    qset=qset((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))


    qset_sum=db()
    qset_sum=qset_sum(db.sm_invoice_head.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice_head.status=='Invoiced')
    qset_sum=qset_sum((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    if (depot_id!=''):
        qset=qset(db.sm_invoice.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice.store_id==store_id)
        qset_sum=qset_sum(db.sm_invoice_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_invoice.client_id==customer_id)
        qset_sum=qset_sum(db.sm_invoice_head.client_id==customer_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_invoice.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_invoice_head.rep_id==mso_id)
    if (market_id!=''):
        qset=qset(db.sm_invoice.market_id==market_id)
        qset_sum=qset_sum(db.sm_invoice_head.market_id==market_id)
        
    if (teritory_id!=''):
       qset=qset(db.sm_invoice.area_id==teritory_id)
       qset_sum=qset_sum(db.sm_invoice_head.area_id==teritory_id)
    
    records=qset.select(db.sm_invoice.item_id,db.sm_invoice.item_name,db.sm_invoice.actual_tp,db.sm_invoice.return_rate,db.sm_invoice.item_vat,(db.sm_invoice.item_vat*db.sm_invoice.quantity).sum(),(db.sm_invoice.item_vat*db.sm_invoice.return_qty).sum(),db.sm_invoice.quantity.sum(),db.sm_invoice.price,db.sm_invoice.item_vat,(db.sm_invoice.actual_tp *db.sm_invoice.return_qty).sum(),(db.sm_invoice.actual_tp *db.sm_invoice.return_qty).sum(),(db.sm_invoice.return_rate *db.sm_invoice.return_qty).sum(),(db.sm_invoice.quantity*db.sm_invoice.actual_tp).sum(),(db.sm_invoice.quantity*db.sm_invoice.price).sum(),(db.sm_invoice.return_qty*db.sm_invoice.price).sum(),db.sm_invoice.bonus_qty.sum(),db.sm_invoice.return_qty.sum(),db.sm_invoice.return_bonus_qty.sum(),orderby=db.sm_invoice.item_name | ~db.sm_invoice.item_vat,groupby=db.sm_invoice.item_id)
   
    
    condition_ret=''
    if (depot_id!=''):
        condition_ret=condition_ret+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition_ret=condition_ret+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition_ret=condition_ret+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition_ret=condition_ret+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition_ret=condition_ret+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition_ret=condition_ret+"AND area_id= '"+str(teritory_id)+"'"
    
    records_retS="SELECT  sum(item_vat * (quantity-return_qty)) as vat_amnt, sum(quantity) as inv_qty ,sum(bonus_qty) as inv_bonus_qty,sum(quantity * actual_tp) as inv_tp,sum(quantity * actual_tp) as inv_amnt,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty,sum(return_qty * actual_tp) as ret_amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+condition_ret+"  limit  1;"
    records_ret=db.executesql(records_retS,as_dict = True) 

    if records:
        for records_ret in records_ret:
            vat_amnt=records_ret['vat_amnt']
            inv_qty=records_ret['inv_qty']
            inv_bonus_qty=records_ret['inv_bonus_qty']
            inv_tp=records_ret['inv_tp']
            inv_amnt=records_ret['inv_amnt']
            ret_qty=records_ret['ret_qty']
            ret_bonus_qty=records_ret['ret_bonus_qty']
            ret_amnt=records_ret['ret_amnt']
            vat_amnt=records_ret['vat_amnt']
            

            rtnP_total=(ret_amnt*100)/inv_amnt
            nsP_total =((inv_amnt-ret_amnt) *100)/inv_amnt
            
            
            
            
            rtnP_total=(ret_amnt*100)/inv_amnt
            
#         return ret_amnt
        record_sum=qset_sum.select((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_discount).sum(),db.sm_invoice_head.total_amount.sum(),(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),(db.sm_invoice_head.return_discount).sum(),(db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_vat.sum(), limitby=(0,1))
#         return db._lastsql
        total=0.0
       
        
        for rec in record_sum:          
            disc=rec[db.sm_invoice_head.discount.sum()]-rec[db.sm_invoice_head.return_discount.sum()]
            spdisc=rec[db.sm_invoice_head.sp_discount.sum()]
            retdisc=rec[db.sm_invoice_head.return_sp_discount.sum()]

    
        invList = []
        invList_str = []
        
        retList = []
        retList_str = []
    
        qsetInv=db()
        qsetInv=qsetInv(db.sm_invoice_head.cid==c_id)
        qsetInv=qsetInv(db.sm_invoice.cid==db.sm_invoice_head.cid)
        qsetInv=qsetInv(db.sm_invoice.sl==db.sm_invoice_head.sl)
        qsetInv=qsetInv(db.sm_invoice.depot_id==db.sm_invoice_head.depot_id)
        qsetInv=qsetInv(db.sm_invoice.status=='Invoiced')
        qsetInv=qsetInv((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
        
        
        qsetRet=db()
        qsetRet=qsetRet(db.sm_invoice_head.cid==c_id)
        qsetRet=qsetRet(db.sm_invoice.cid==db.sm_invoice_head.cid)
        qsetRet=qsetRet(db.sm_invoice.sl==db.sm_invoice_head.sl)
        qsetRet=qsetRet(db.sm_invoice.depot_id==db.sm_invoice_head.depot_id)
        qsetRet=qsetRet(db.sm_invoice.status=='Invoiced')
        qsetRet=qsetRet(db.sm_invoice.return_qty!=0)
        qsetRet=qsetRet((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
        
        if (depot_id!=''):
            qsetInv=qsetInv(db.sm_invoice.depot_id==depot_id)  
            qsetRet=qsetRet(db.sm_invoice.depot_id==depot_id)   
        if (store_id!=''):
            qsetInv=qsetInv(db.sm_invoice.store_id==store_id)
            qsetRet=qsetRet(db.sm_invoice.store_id==store_id)
            
        if (customer_id!=''):
            qsetInv=qsetInv(db.sm_invoice.client_id==customer_id)
            qsetRet=qsetRet(db.sm_invoice.client_id==customer_id)
         
        if (mso_id!=''):
            qsetInv=qsetInv(db.sm_invoice.rep_id==mso_id)
            qsetRet=qsetRet(db.sm_invoice.rep_id==mso_id)
        if (market_id!=''):
            qsetInv=qsetInv(db.sm_invoice.market_id==market_id)
            qsetRet=qsetRet(db.sm_invoice.market_id==market_id)
            
            
      
        invCountRows=qsetInv.select(db.sm_invoice.item_id,db.sm_invoice_head.sl.count(),orderby=db.sm_invoice.item_name,groupby=db.sm_invoice.item_id)
        
        retCountRows=qsetRet.select(db.sm_invoice.item_id,db.sm_invoice_head.sl.count(),orderby=db.sm_invoice.item_name,groupby=db.sm_invoice.item_id)
    #     return invCountRows
        for invCountRows in invCountRows:
            item_id = invCountRows[db.sm_invoice.item_id]
            invCount = invCountRows[db.sm_invoice_head.sl.count()]
            invList.append(item_id)
            invList_str.append(invCount)
        
        for retCountRows in retCountRows:
            retitem_id = retCountRows[db.sm_invoice.item_id]
            retCount = retCountRows[db.sm_invoice_head.sl.count()]
            retList.append(retitem_id)
            retList_str.append(retCount)
            
        
        return dict(records=records,invList=invList,invList_str=invList_str,retList=retList,retList_str=retList_str,disc=disc,spdisc=spdisc,retdisc=retdisc,vat_amnt=vat_amnt,inv_qty=inv_qty,inv_bonus_qty=inv_bonus_qty,inv_tp=inv_tp,inv_amnt=inv_amnt,ret_qty=ret_qty,ret_bonus_qty=ret_bonus_qty,ret_amnt=ret_amnt,rtnP_total=rtnP_total,nsP_total=nsP_total,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,teritory_id=teritory_id,teritory_name=teritory_name,total=total,page=page,items_per_page=items_per_page)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
           
def itemWiseSalesSDetailDLoad():
    c_id=session.cid
    response.title='Item Wise Sales Statement Detail'
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
   
    qset=db()
    qset=qset(db.sm_invoice.cid==c_id)
    qset=qset(db.sm_invoice.status=='Invoiced')
    qset=qset((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))


    qset_sum=db()
    qset_sum=qset_sum(db.sm_invoice_head.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice_head.status=='Invoiced')
    qset_sum=qset_sum((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    if (depot_id!=''):
        qset=qset(db.sm_invoice.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice.store_id==store_id)
        qset_sum=qset_sum(db.sm_invoice_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_invoice.client_id==customer_id)
        qset_sum=qset_sum(db.sm_invoice_head.client_id==customer_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_invoice.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_invoice_head.rep_id==mso_id)
    if (market_id!=''):
        qset=qset(db.sm_invoice.market_id==market_id)
        qset_sum=qset_sum(db.sm_invoice_head.market_id==market_id)
        
    if (teritory_id!=''):
       qset=qset(db.sm_invoice.area_id==teritory_id)
       qset_sum=qset_sum(db.sm_invoice_head.area_id==teritory_id)
    
    records=qset.select(db.sm_invoice.item_id,db.sm_invoice.item_name,db.sm_invoice.actual_tp,db.sm_invoice.return_rate,db.sm_invoice.item_vat,(db.sm_invoice.item_vat*db.sm_invoice.quantity).sum(),(db.sm_invoice.item_vat*db.sm_invoice.return_qty).sum(),db.sm_invoice.quantity.sum(),db.sm_invoice.price,db.sm_invoice.item_vat,(db.sm_invoice.actual_tp *db.sm_invoice.return_qty).sum(),(db.sm_invoice.actual_tp *db.sm_invoice.return_qty).sum(),(db.sm_invoice.return_rate *db.sm_invoice.return_qty).sum(),(db.sm_invoice.quantity*db.sm_invoice.actual_tp).sum(),(db.sm_invoice.quantity*db.sm_invoice.price).sum(),(db.sm_invoice.return_qty*db.sm_invoice.price).sum(),db.sm_invoice.bonus_qty.sum(),db.sm_invoice.return_qty.sum(),db.sm_invoice.return_bonus_qty.sum(),orderby=db.sm_invoice.item_name | ~db.sm_invoice.item_vat,groupby=db.sm_invoice.item_id)
   
    
    condition_ret=''
    if (depot_id!=''):
        condition_ret=condition_ret+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition_ret=condition_ret+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition_ret=condition_ret+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition_ret=condition_ret+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition_ret=condition_ret+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition_ret=condition_ret+"AND area_id= '"+str(teritory_id)+"'"
    
    records_retS="SELECT  sum(item_vat * (quantity-return_qty)) as vat_amnt, sum(quantity) as inv_qty ,sum(bonus_qty) as inv_bonus_qty,sum(quantity * actual_tp) as inv_tp,sum(quantity * actual_tp) as inv_amnt,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty,sum(return_qty * actual_tp) as ret_amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+condition_ret+"  limit  1;"
    records_ret=db.executesql(records_retS,as_dict = True) 

    if records:
        for records_ret in records_ret:
            vat_amnt=records_ret['vat_amnt']
            inv_qty=records_ret['inv_qty']
            inv_bonus_qty=records_ret['inv_bonus_qty']
            inv_tp=records_ret['inv_tp']
            inv_amnt=records_ret['inv_amnt']
            ret_qty=records_ret['ret_qty']
            ret_bonus_qty=records_ret['ret_bonus_qty']
            ret_amnt=records_ret['ret_amnt']
            vat_amnt=records_ret['vat_amnt']
            

            rtnP_total=(ret_amnt*100)/inv_amnt
            nsP_total =((inv_amnt-ret_amnt) *100)/inv_amnt
            
            
            
            
            rtnP_total=(ret_amnt*100)/inv_amnt
            
#         return ret_amnt
        record_sum=qset_sum.select((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_discount).sum(),db.sm_invoice_head.total_amount.sum(),(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),(db.sm_invoice_head.return_discount).sum(),(db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_vat.sum(), limitby=(0,1))
#         return db._lastsql
        total=0.0
       
        
        for rec in record_sum:          
            disc=rec[db.sm_invoice_head.discount.sum()]-rec[db.sm_invoice_head.return_discount.sum()]
            spdisc=rec[db.sm_invoice_head.sp_discount.sum()]
            retdisc=rec[db.sm_invoice_head.return_sp_discount.sum()]

    
        invList = []
        invList_str = []
        
        retList = []
        retList_str = []
    
        qsetInv=db()
        qsetInv=qsetInv(db.sm_invoice_head.cid==c_id)
        qsetInv=qsetInv(db.sm_invoice.cid==db.sm_invoice_head.cid)
        qsetInv=qsetInv(db.sm_invoice.sl==db.sm_invoice_head.sl)
        qsetInv=qsetInv(db.sm_invoice.depot_id==db.sm_invoice_head.depot_id)
        qsetInv=qsetInv(db.sm_invoice.status=='Invoiced')
        qsetInv=qsetInv((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
        
        
        qsetRet=db()
        qsetRet=qsetRet(db.sm_invoice_head.cid==c_id)
        qsetRet=qsetRet(db.sm_invoice.cid==db.sm_invoice_head.cid)
        qsetRet=qsetRet(db.sm_invoice.sl==db.sm_invoice_head.sl)
        qsetRet=qsetRet(db.sm_invoice.depot_id==db.sm_invoice_head.depot_id)
        qsetRet=qsetRet(db.sm_invoice.status=='Invoiced')
        qsetRet=qsetRet(db.sm_invoice.return_qty!=0)
        qsetRet=qsetRet((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
        
        if (depot_id!=''):
            qsetInv=qsetInv(db.sm_invoice.depot_id==depot_id)  
            qsetRet=qsetRet(db.sm_invoice.depot_id==depot_id)   
        if (store_id!=''):
            qsetInv=qsetInv(db.sm_invoice.store_id==store_id)
            qsetRet=qsetRet(db.sm_invoice.store_id==store_id)
            
        if (customer_id!=''):
            qsetInv=qsetInv(db.sm_invoice.client_id==customer_id)
            qsetRet=qsetRet(db.sm_invoice.client_id==customer_id)
         
        if (mso_id!=''):
            qsetInv=qsetInv(db.sm_invoice.rep_id==mso_id)
            qsetRet=qsetRet(db.sm_invoice.rep_id==mso_id)
        if (market_id!=''):
            qsetInv=qsetInv(db.sm_invoice.market_id==market_id)
            qsetRet=qsetRet(db.sm_invoice.market_id==market_id)
            
            
      
        invCountRows=qsetInv.select(db.sm_invoice.item_id,db.sm_invoice_head.sl.count(),orderby=db.sm_invoice.item_name,groupby=db.sm_invoice.item_id)
        
        retCountRows=qsetRet.select(db.sm_invoice.item_id,db.sm_invoice_head.sl.count(),orderby=db.sm_invoice.item_name,groupby=db.sm_invoice.item_id)
    #     return invCountRows
        for invCountRows in invCountRows:
            item_id = invCountRows[db.sm_invoice.item_id]
            invCount = invCountRows[db.sm_invoice_head.sl.count()]
            invList.append(item_id)
            invList_str.append(invCount)
        
        for retCountRows in retCountRows:
            retitem_id = retCountRows[db.sm_invoice.item_id]
            retCount = retCountRows[db.sm_invoice_head.sl.count()]
            retList.append(retitem_id)
            retList_str.append(retCount)
            
       
       
       
        myString='Item Wise Sales Statement Detail\n'
        myString=myString+'Depot/Branch,'+date_from+'|'+date_to+'\n'
        myString=myString+'Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString=myString+'Store,'+store_id+'|'+store_name+'\n'
        myString=myString+'Customer,'+customer_id+'|'+customer_name+'\n'
        myString=myString+'Teritory,'+teritory_id+'|'+teritory_name+'\n'
        myString=myString+'MSO,'+mso_id+'|'+mso_name+'\n\n'
        
        myString=myString+'Invoice: ,S.Qty,'+str(inv_qty)+',B.Qty,'+str(inv_bonus_qty)+',TP,'+str(round(inv_tp,2))+'\n'
        myString=myString+'Return: ,S.Qty,'+str(ret_qty)+',B.Qty,'+str(ret_bonus_qty)+',TP,'+str(round(ret_amnt,2))+''+',RTN%,'+str(round(rtnP_total,2))+'\n'
        myString=myString+'Net Sales: ,S.Qty,'+str(inv_qty-ret_qty)+',B.Qty,'+str(inv_bonus_qty-ret_bonus_qty)+',TP,'+str(round((inv_tp-ret_amnt),2))+',SPDisc,'+str(round((float(inv_tp)-float(inv_amnt)),2))+',Net,'+str(round(inv_amnt-ret_amnt,2))+',NS%,'+str(round(nsP_total,2))+'\n'
        
        myString+='Item,ItemName,InvCount,RetCount, InvS.Qty,InvB.Qty,InvTP,RetS.Qty,RetB.Qty,RetTP,RTN%,NetS.Qty,NetB.Qty,NetTP,Vat,Net (TP+Vat),NS%\n'
          
        for record in records:
            itmInv=0
            itmRet=0
            item_id =record[db.sm_invoice.item_id]
            if [s for s in invList if item_id in s]:
                index_element = invList.index(item_id)           
                itmInv=invList_str[index_element]
            if [s for s in retList if item_id in s]:
                ret_index_element = retList.index(item_id)           
                itmRet=retList_str[ret_index_element]
            invSale= float(record[db.sm_invoice.quantity.sum()]* record[db.sm_invoice.actual_tp])
            netRet= record[db.sm_invoice.return_qty.sum()]* record[db.sm_invoice.actual_tp]
            rtnP=0
               
            if (invSale > 0):
                rtnP=(netRet*100)/invSale
            netQty=int(record[db.sm_invoice.quantity.sum()])-int(record[db.sm_invoice.return_qty.sum()])
            netSale  =  invSale-netRet 
            vat=record[(db.sm_invoice.item_vat*db.sm_invoice.quantity).sum()]-record[(db.sm_invoice.item_vat*db.sm_invoice.return_qty).sum()]
            nsP=0
            if (invSale > 0):
                nsP =(netSale *100)/invSale
                                                                                                                                        
       
                                                                                                                                                                
            myString+=str(record[db.sm_invoice.item_id])+','+str(record[db.sm_invoice.item_name])+','+str(itmInv)+','+str(itmRet)+','+str(record[db.sm_invoice.quantity.sum()])+','+str(record[db.sm_invoice.bonus_qty.sum()])+','+str(record[db.sm_invoice.quantity.sum()]* record[db.sm_invoice.actual_tp])+','+str(record[db.sm_invoice.return_qty.sum()])+','+str(record[db.sm_invoice.return_bonus_qty.sum()])+','+str(record[db.sm_invoice.return_qty.sum()]* record[db.sm_invoice.actual_tp])+','+str(rtnP)+','+str(netQty)+','+str(int(record[db.sm_invoice.bonus_qty.sum()])-int(record[db.sm_invoice.return_bonus_qty.sum()]))+','+str(invSale - netRet)+','+str(vat)+','+str(netSale+vat)+','+str(nsP)+'\n'
#         return myString
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=ItemWiseSalesStatementDetail.csv'   
        return str(myString)  
        
#         return dict(records=records,invList=invList,invList_str=invList_str,retList=retList,retList_str=retList_str,vat_amnt=vat_amnt,inv_qty=inv_qty,inv_bonus_qty=inv_bonus_qty,inv_amnt=inv_amnt,ret_qty=ret_qty,ret_bonus_qty=ret_bonus_qty,ret_amnt=ret_amnt,rtnP_total=rtnP_total,nsP_total=nsP_total,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,total=total,page=page,items_per_page=items_per_page)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
def itemWiseSalesSDetailLand():
    c_id=session.cid
    response.title='Item Wise Sales Statement Detail'
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
   
    qset=db()
    qset=qset(db.sm_invoice.cid==c_id)
    qset=qset(db.sm_invoice.status=='Invoiced')
    qset=qset((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))


    qset_sum=db()
    qset_sum=qset_sum(db.sm_invoice_head.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice_head.status=='Invoiced')
    qset_sum=qset_sum((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    if (depot_id!=''):
        qset=qset(db.sm_invoice.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice.store_id==store_id)
        qset_sum=qset_sum(db.sm_invoice_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_invoice.client_id==customer_id)
        qset_sum=qset_sum(db.sm_invoice_head.client_id==customer_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_invoice.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_invoice_head.rep_id==mso_id)
    if (market_id!=''):
        qset=qset(db.sm_invoice.market_id==market_id)
        qset_sum=qset_sum(db.sm_invoice_head.market_id==market_id)
        
    if (teritory_id!=''):
       qset=qset(db.sm_invoice.area_id==teritory_id)
       qset_sum=qset_sum(db.sm_invoice_head.area_id==teritory_id)
    
    records=qset.select(db.sm_invoice.item_id,db.sm_invoice.item_name,db.sm_invoice.actual_tp,db.sm_invoice.return_rate,db.sm_invoice.item_vat,(db.sm_invoice.item_vat*db.sm_invoice.quantity).sum(),(db.sm_invoice.item_vat*db.sm_invoice.return_qty).sum(),db.sm_invoice.quantity.sum(),db.sm_invoice.price,db.sm_invoice.item_vat,(db.sm_invoice.actual_tp *db.sm_invoice.return_qty).sum(),(db.sm_invoice.actual_tp *db.sm_invoice.return_qty).sum(),(db.sm_invoice.return_rate *db.sm_invoice.return_qty).sum(),(db.sm_invoice.quantity*db.sm_invoice.actual_tp).sum(),(db.sm_invoice.quantity*db.sm_invoice.price).sum(),(db.sm_invoice.return_qty*db.sm_invoice.price).sum(),db.sm_invoice.bonus_qty.sum(),db.sm_invoice.return_qty.sum(),db.sm_invoice.return_bonus_qty.sum(),orderby=db.sm_invoice.item_name | ~db.sm_invoice.item_vat,groupby=db.sm_invoice.item_id)
   
    
    condition_ret=''
    if (depot_id!=''):
        condition_ret=condition_ret+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition_ret=condition_ret+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition_ret=condition_ret+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition_ret=condition_ret+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition_ret=condition_ret+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition_ret=condition_ret+"AND area_id= '"+str(teritory_id)+"'"
    
    records_retS="SELECT  sum(item_vat * (quantity-return_qty)) as vat_amnt, sum(quantity) as inv_qty ,sum(bonus_qty) as inv_bonus_qty,sum(quantity * actual_tp) as inv_tp,sum(quantity * actual_tp) as inv_amnt,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty,sum(return_qty * actual_tp) as ret_amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+condition_ret+"  limit  1;"
    records_ret=db.executesql(records_retS,as_dict = True) 

    if records:
        for records_ret in records_ret:
            vat_amnt=records_ret['vat_amnt']
            inv_qty=records_ret['inv_qty']
            inv_bonus_qty=records_ret['inv_bonus_qty']
            inv_tp=records_ret['inv_tp']
            inv_amnt=records_ret['inv_amnt']
            ret_qty=records_ret['ret_qty']
            ret_bonus_qty=records_ret['ret_bonus_qty']
            ret_amnt=records_ret['ret_amnt']
            vat_amnt=records_ret['vat_amnt']
            

            rtnP_total=(ret_amnt*100)/inv_amnt
            nsP_total =((inv_amnt-ret_amnt) *100)/inv_amnt
            
            
            
            
            rtnP_total=(ret_amnt*100)/inv_amnt
            
#         return ret_amnt
        record_sum=qset_sum.select((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_discount).sum(),db.sm_invoice_head.total_amount.sum(),(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),(db.sm_invoice_head.return_discount).sum(),(db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_vat.sum(), limitby=(0,1))
#         return db._lastsql
        total=0.0
       
        
        for rec in record_sum:          
            disc=rec[db.sm_invoice_head.discount.sum()]-rec[db.sm_invoice_head.return_discount.sum()]
            spdisc=rec[db.sm_invoice_head.sp_discount.sum()]
            retdisc=rec[db.sm_invoice_head.return_sp_discount.sum()]

    
        invList = []
        invList_str = []
        
        retList = []
        retList_str = []
    
        qsetInv=db()
        qsetInv=qsetInv(db.sm_invoice_head.cid==c_id)
        qsetInv=qsetInv(db.sm_invoice.cid==db.sm_invoice_head.cid)
        qsetInv=qsetInv(db.sm_invoice.sl==db.sm_invoice_head.sl)
        qsetInv=qsetInv(db.sm_invoice.depot_id==db.sm_invoice_head.depot_id)
        qsetInv=qsetInv(db.sm_invoice.status=='Invoiced')
        qsetInv=qsetInv((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
        
        
        qsetRet=db()
        qsetRet=qsetRet(db.sm_invoice_head.cid==c_id)
        qsetRet=qsetRet(db.sm_invoice.cid==db.sm_invoice_head.cid)
        qsetRet=qsetRet(db.sm_invoice.sl==db.sm_invoice_head.sl)
        qsetRet=qsetRet(db.sm_invoice.depot_id==db.sm_invoice_head.depot_id)
        qsetRet=qsetRet(db.sm_invoice.status=='Invoiced')
        qsetRet=qsetRet(db.sm_invoice.return_qty!=0)
        qsetRet=qsetRet((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
        
        if (depot_id!=''):
            qsetInv=qsetInv(db.sm_invoice.depot_id==depot_id)  
            qsetRet=qsetRet(db.sm_invoice.depot_id==depot_id)   
        if (store_id!=''):
            qsetInv=qsetInv(db.sm_invoice.store_id==store_id)
            qsetRet=qsetRet(db.sm_invoice.store_id==store_id)
            
        if (customer_id!=''):
            qsetInv=qsetInv(db.sm_invoice.client_id==customer_id)
            qsetRet=qsetRet(db.sm_invoice.client_id==customer_id)
         
        if (mso_id!=''):
            qsetInv=qsetInv(db.sm_invoice.rep_id==mso_id)
            qsetRet=qsetRet(db.sm_invoice.rep_id==mso_id)
        if (market_id!=''):
            qsetInv=qsetInv(db.sm_invoice.market_id==market_id)
            qsetRet=qsetRet(db.sm_invoice.market_id==market_id)
            
            
      
        invCountRows=qsetInv.select(db.sm_invoice.item_id,db.sm_invoice_head.sl.count(),orderby=db.sm_invoice.item_name,groupby=db.sm_invoice.item_id)
        
        retCountRows=qsetRet.select(db.sm_invoice.item_id,db.sm_invoice_head.sl.count(),orderby=db.sm_invoice.item_name,groupby=db.sm_invoice.item_id)
    #     return invCountRows
        for invCountRows in invCountRows:
            item_id = invCountRows[db.sm_invoice.item_id]
            invCount = invCountRows[db.sm_invoice_head.sl.count()]
            invList.append(item_id)
            invList_str.append(invCount)
        
        for retCountRows in retCountRows:
            retitem_id = retCountRows[db.sm_invoice.item_id]
            retCount = retCountRows[db.sm_invoice_head.sl.count()]
            retList.append(retitem_id)
            retList_str.append(retCount)
            
        
        return dict(records=records,invList=invList,invList_str=invList_str,retList=retList,retList_str=retList_str,disc=disc,spdisc=spdisc,retdisc=retdisc,vat_amnt=vat_amnt,inv_qty=inv_qty,inv_bonus_qty=inv_bonus_qty,inv_tp=inv_tp,inv_amnt=inv_amnt,ret_qty=ret_qty,ret_bonus_qty=ret_bonus_qty,ret_amnt=ret_amnt,rtnP_total=rtnP_total,nsP_total=nsP_total,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,teritory_id=teritory_id,teritory_name=teritory_name,total=total,page=page,items_per_page=items_per_page)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
           
def invoiceWiseSalesSDetail():
    c_id=session.cid
    response.title='Invoice Wise Sales Statement Detail'
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
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
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))


    qset_sum=db()
    qset_sum=qset_sum(db.sm_invoice_head.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice_head.status=='Invoiced')
    qset_sum=qset_sum((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    if (depot_id!=''):
        qset=qset(db.sm_invoice_head.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice_head.store_id==store_id)
        qset_sum=qset_sum(db.sm_invoice_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_invoice_head.client_id==customer_id)
        qset_sum=qset_sum(db.sm_invoice_head.client_id==customer_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_invoice_head.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_invoice_head.rep_id==mso_id)
    if (market_id!=''):
        qset=qset(db.sm_invoice_head.market_id==market_id)
        qset_sum=qset_sum(db.sm_invoice_head.market_id==market_id)
        
    if (teritory_id!=''):
       qset=qset(db.sm_invoice_head.area_id==teritory_id)
       qset_sum=qset_sum(db.sm_invoice_head.area_id==teritory_id)
    
    records=qset.select(db.sm_invoice_head.invoice_date,db.sm_invoice_head.sl,db.sm_invoice_head.depot_id,db.sm_invoice_head.client_id,db.sm_invoice_head.client_name,db.sm_invoice_head.rep_id,db.sm_invoice_head.rep_name,db.sm_invoice_head.market_id,db.sm_invoice_head.market_name,db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_sp_discount.sum(),db.sm_invoice_head.return_discount.sum(),orderby=db.sm_invoice_head.sl,groupby=db.sm_invoice_head.sl)
   
    
    condition_ret=''
    if (depot_id!=''):
        condition_ret=condition_ret+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition_ret=condition_ret+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition_ret=condition_ret+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition_ret=condition_ret+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition_ret=condition_ret+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition_ret=condition_ret+"AND area_id= '"+str(teritory_id)+"'"
    
    records_retS="SELECT  sum(item_vat * (quantity-return_qty)) as vat_amnt, sum(quantity) as inv_qty ,sum(bonus_qty) as inv_bonus_qty,sum(quantity * actual_tp) as inv_tp,sum(quantity * actual_tp) as inv_amnt,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty,sum(return_qty * actual_tp) as ret_amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+condition_ret+"  limit  1;"
    records_ret=db.executesql(records_retS,as_dict = True) 

    if records:
        for records_ret in records_ret:
            vat_amnt=records_ret['vat_amnt']
            inv_qty=records_ret['inv_qty']
            inv_bonus_qty=records_ret['inv_bonus_qty']
            inv_tp=records_ret['inv_tp']
            inv_amnt=records_ret['inv_amnt']
            ret_qty=records_ret['ret_qty']
            ret_bonus_qty=records_ret['ret_bonus_qty']
            ret_amnt=records_ret['ret_amnt']
            vat_amnt=records_ret['vat_amnt']
            

            rtnP_total=(ret_amnt*100)/inv_amnt
            nsP_total =((inv_amnt-ret_amnt) *100)/inv_amnt
            
            
            
            
            rtnP_total=(ret_amnt*100)/inv_amnt
            
#         return ret_amnt
        record_sum=qset_sum.select((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_discount).sum(),db.sm_invoice_head.total_amount.sum(),(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),(db.sm_invoice_head.return_discount).sum(),(db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_vat.sum(), limitby=(0,1))
#         return db._lastsql
        total=0.0
       
        
        for rec in record_sum:          
            disc=rec[db.sm_invoice_head.discount.sum()]-rec[db.sm_invoice_head.return_discount.sum()]
            spdisc=rec[db.sm_invoice_head.sp_discount.sum()]
            retdisc=rec[db.sm_invoice_head.return_sp_discount.sum()]

    
        
        
        
            
        
        return dict(records=records,disc=disc,spdisc=spdisc,retdisc=retdisc,vat_amnt=vat_amnt,inv_qty=inv_qty,inv_bonus_qty=inv_bonus_qty,inv_tp=inv_tp,inv_amnt=inv_amnt,ret_qty=ret_qty,ret_bonus_qty=ret_bonus_qty,ret_amnt=ret_amnt,rtnP_total=rtnP_total,nsP_total=nsP_total,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,teritory_id=teritory_id,teritory_name=teritory_name,total=total,page=page,items_per_page=items_per_page)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))


def invoiceWiseSalesSDetailD():
    c_id=session.cid
    response.title='Invoice Wise Sales Statement Detail'
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
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
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))


    qset_sum=db()
    qset_sum=qset_sum(db.sm_invoice_head.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice_head.status=='Invoiced')
    qset_sum=qset_sum((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    if (depot_id!=''):
        qset=qset(db.sm_invoice_head.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice_head.store_id==store_id)
        qset_sum=qset_sum(db.sm_invoice_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_invoice_head.client_id==customer_id)
        qset_sum=qset_sum(db.sm_invoice_head.client_id==customer_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_invoice_head.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_invoice_head.rep_id==mso_id)
    if (market_id!=''):
        qset=qset(db.sm_invoice_head.market_id==market_id)
        qset_sum=qset_sum(db.sm_invoice_head.market_id==market_id)
        
    if (teritory_id!=''):
       qset=qset(db.sm_invoice_head.area_id==teritory_id)
       qset_sum=qset_sum(db.sm_invoice_head.area_id==teritory_id)
    
    records=qset.select(db.sm_invoice_head.invoice_date,db.sm_invoice_head.sl,db.sm_invoice_head.depot_id,db.sm_invoice_head.client_id,db.sm_invoice_head.client_name,db.sm_invoice_head.rep_id,db.sm_invoice_head.rep_name,db.sm_invoice_head.market_id,db.sm_invoice_head.market_name,db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_sp_discount.sum(),db.sm_invoice_head.return_discount.sum(),orderby=db.sm_invoice_head.sl,groupby=db.sm_invoice_head.sl)
   
    
    condition_ret=''
    if (depot_id!=''):
        condition_ret=condition_ret+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition_ret=condition_ret+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition_ret=condition_ret+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition_ret=condition_ret+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition_ret=condition_ret+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition_ret=condition_ret+"AND area_id= '"+str(teritory_id)+"'"
    
    records_retS="SELECT  sum(item_vat * (quantity-return_qty)) as vat_amnt, sum(quantity) as inv_qty ,sum(bonus_qty) as inv_bonus_qty,sum(quantity * actual_tp) as inv_tp,sum(quantity * actual_tp) as inv_amnt,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty,sum(return_qty * actual_tp) as ret_amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+condition_ret+"  limit  1;"
    records_ret=db.executesql(records_retS,as_dict = True) 

    if records:
        for records_ret in records_ret:
            vat_amnt=records_ret['vat_amnt']
            inv_qty=records_ret['inv_qty']
            inv_bonus_qty=records_ret['inv_bonus_qty']
            inv_tp=records_ret['inv_tp']
            inv_amnt=records_ret['inv_amnt']
            ret_qty=records_ret['ret_qty']
            ret_bonus_qty=records_ret['ret_bonus_qty']
            ret_amnt=records_ret['ret_amnt']
            vat_amnt=records_ret['vat_amnt']
            

            rtnP_total=(ret_amnt*100)/inv_amnt
            nsP_total =((inv_amnt-ret_amnt) *100)/inv_amnt
            
            
            
            
            rtnP_total=(ret_amnt*100)/inv_amnt
            
#         return ret_amnt
        record_sum=qset_sum.select((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_discount).sum(),db.sm_invoice_head.total_amount.sum(),(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),(db.sm_invoice_head.return_discount).sum(),(db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_vat.sum(), limitby=(0,1))
#         return db._lastsql
        total=0.0
       
        
        for rec in record_sum:          
            disc=rec[db.sm_invoice_head.discount.sum()]-rec[db.sm_invoice_head.return_discount.sum()]
            spdisc=rec[db.sm_invoice_head.sp_discount.sum()]
            retdisc=rec[db.sm_invoice_head.return_sp_discount.sum()]

    
    if records:
        myString='Inv Wise Sales\n'
        myString=myString+'DateRange,'+date_from+'|'+date_to+'\n'
        myString=myString+'Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString=myString+'Store,'+store_id+'|'+store_name+'\n'
        myString=myString+'Customer,'+customer_id+'|'+customer_name+'\n'
        myString=myString+'Teritory,'+teritory_id+'|'+teritory_name+'\n\n'
        myString=myString+'MSO,'+mso_id+'|'+mso_name+'\n\n'
         
       
         
        myString+='Date  ,  Inv Number  ,  CustomerID, CustomerName  ,  MSOID, MSO Name  ,  Market  ,  InvTP   , InvDisc  ,  InvVat  ,  InvNet ,   RetTP  ,  RetDisc  ,  RetVat   , RetNet  ,  NetTP  ,  NetDisc  ,  NetVat  ,  Net\n'
          
        for record in records: 

            retNet=record[db.sm_invoice_head.return_tp.sum()]+record[db.sm_invoice_head.return_vat.sum()]-(record[db.sm_invoice_head.return_sp_discount.sum()]+record[db.sm_invoice_head.return_discount.sum()])
            inv= 'INV'+str(record[db.sm_invoice_head.depot_id])+'-'+str(record[db.sm_invoice_head.sl])
            myString=myString+str(record[db.sm_invoice_head.invoice_date])+','+str(inv)+','+str(record[db.sm_invoice_head.client_id])+','+str(record[db.sm_invoice_head.client_name])+','+str(record[db.sm_invoice_head.rep_id])+','+str(record[db.sm_invoice_head.rep_name])+','+str(record[db.sm_invoice_head.market_id])+','+str(record[db.sm_invoice_head.actual_total_tp.sum()])+','+str(record[db.sm_invoice_head.discount.sum()]+record[db.sm_invoice_head.sp_discount.sum()])+','+str(record[db.sm_invoice_head.vat_total_amount.sum()])+','+str(record[db.sm_invoice_head.total_amount.sum()])+','+str(record[db.sm_invoice_head.return_tp.sum()])+','+str(record[db.sm_invoice_head.return_sp_discount.sum()]+record[db.sm_invoice_head.return_discount.sum()])+','+str(record[db.sm_invoice_head.return_vat.sum()])+','+str(retNet)+','+str(record[db.sm_invoice_head.actual_total_tp.sum()]-record[db.sm_invoice_head.return_tp.sum()])+','+str((record[db.sm_invoice_head.discount.sum()]+record[db.sm_invoice_head.sp_discount.sum()])-(record[db.sm_invoice_head.return_sp_discount.sum()]+record[db.sm_invoice_head.return_discount.sum()]))+','+str(record[db.sm_invoice_head.vat_total_amount.sum()]-record[db.sm_invoice_head.return_vat.sum()])+','+str(record[db.sm_invoice_head.total_amount.sum()]-retNet)+'\n'
         
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=InvWiseSalesStatementDetail.csv'   
        return str(myString)
       
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))


# --------------------------------------------------
def customerWiseSalesSDetail():
    c_id=session.cid
    response.title='Customer Wise Sales Statement Detail'
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
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
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))


    qset_sum=db()
    qset_sum=qset_sum(db.sm_invoice_head.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice_head.status=='Invoiced')
    qset_sum=qset_sum((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    if (depot_id!=''):
        qset=qset(db.sm_invoice_head.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice_head.store_id==store_id)
        qset_sum=qset_sum(db.sm_invoice_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_invoice_head.client_id==customer_id)
        qset_sum=qset_sum(db.sm_invoice_head.client_id==customer_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_invoice_head.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_invoice_head.rep_id==mso_id)
    if (market_id!=''):
        qset=qset(db.sm_invoice_head.market_id==market_id)
        qset_sum=qset_sum(db.sm_invoice_head.market_id==market_id)
        
    if (teritory_id!=''):
       qset=qset(db.sm_invoice_head.area_id==teritory_id)
       qset_sum=qset_sum(db.sm_invoice_head.area_id==teritory_id)
    
    records=qset.select(db.sm_invoice_head.sl.count(),db.sm_invoice_head.depot_id,db.sm_invoice_head.client_id,db.sm_invoice_head.client_name,db.sm_invoice_head.rep_id,db.sm_invoice_head.rep_name,db.sm_invoice_head.market_id,db.sm_invoice_head.market_name,db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_sp_discount.sum(),db.sm_invoice_head.return_discount.sum(),orderby=db.sm_invoice_head.client_name,groupby=db.sm_invoice_head.client_id)
    
    
    condition_ret=''
    if (depot_id!=''):
        condition_ret=condition_ret+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition_ret=condition_ret+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition_ret=condition_ret+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition_ret=condition_ret+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition_ret=condition_ret+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition_ret=condition_ret+"AND area_id= '"+str(teritory_id)+"'"
    
    records_retS="SELECT  sum(item_vat * (quantity-return_qty)) as vat_amnt, sum(quantity) as inv_qty ,sum(bonus_qty) as inv_bonus_qty,sum(quantity * actual_tp) as inv_tp,sum(quantity * actual_tp) as inv_amnt,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty,sum(return_qty * actual_tp) as ret_amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+condition_ret+"  limit  1;"
    records_ret=db.executesql(records_retS,as_dict = True) 

    if records:
        for records_ret in records_ret:
            vat_amnt=records_ret['vat_amnt']
            inv_qty=records_ret['inv_qty']
            inv_bonus_qty=records_ret['inv_bonus_qty']
            inv_tp=records_ret['inv_tp']
            inv_amnt=records_ret['inv_amnt']
            ret_qty=records_ret['ret_qty']
            ret_bonus_qty=records_ret['ret_bonus_qty']
            ret_amnt=records_ret['ret_amnt']
            vat_amnt=records_ret['vat_amnt']
            

            rtnP_total=(ret_amnt*100)/inv_amnt
            nsP_total =((inv_amnt-ret_amnt) *100)/inv_amnt
            
            
            
            
            rtnP_total=(ret_amnt*100)/inv_amnt
            
#         return ret_amnt
        record_sum=qset_sum.select((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_discount).sum(),db.sm_invoice_head.total_amount.sum(),(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),(db.sm_invoice_head.return_discount).sum(),(db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_vat.sum(), limitby=(0,1))
#         return db._lastsql
        total=0.0
       
        
        for rec in record_sum:          
            disc=rec[db.sm_invoice_head.discount.sum()]-rec[db.sm_invoice_head.return_discount.sum()]
            spdisc=rec[db.sm_invoice_head.sp_discount.sum()]
            retdisc=rec[db.sm_invoice_head.return_sp_discount.sum()]

    
        
        qsetRet=db()
        qsetRet=qsetRet(db.sm_invoice_head.cid==c_id)
        qsetRet=qsetRet(db.sm_invoice.cid==db.sm_invoice_head.cid)
        qsetRet=qsetRet(db.sm_invoice.sl==db.sm_invoice_head.sl)
        qsetRet=qsetRet(db.sm_invoice.depot_id==db.sm_invoice_head.depot_id)
        qsetRet=qsetRet(db.sm_invoice.status=='Invoiced')
        qsetRet=qsetRet(db.sm_invoice.return_qty!=0)
        qsetRet=qsetRet((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
        
        if (depot_id!=''): 
            qsetRet=qsetRet(db.sm_invoice.depot_id==depot_id)   
        if (store_id!=''):
            qsetRet=qsetRet(db.sm_invoice.store_id==store_id)
            
        if (customer_id!=''):
            qsetRet=qsetRet(db.sm_invoice.client_id==customer_id)
         
        if (mso_id!=''):
            qsetRet=qsetRet(db.sm_invoice.rep_id==mso_id)
        if (market_id!=''):
            qsetRet=qsetRet(db.sm_invoice.market_id==market_id)
            
            

        retCountRows=qsetRet.select(db.sm_invoice.client_id,db.sm_invoice_head.sl.count(),orderby=db.sm_invoice.client_name,groupby=db.sm_invoice.client_id)
    #     return invCountRows
        
        retList=[]
        retList_str=[]
        for retCountRows in retCountRows:
            retCust_id = retCountRows[db.sm_invoice.client_id]
            retCount = retCountRows[db.sm_invoice_head.sl.count()]
            retList.append(retCust_id)
            retList_str.append(retCount)
        
            
        
        return dict(records=records,retList=retList,retList_str=retList_str,disc=disc,spdisc=spdisc,retdisc=retdisc,vat_amnt=vat_amnt,inv_qty=inv_qty,inv_bonus_qty=inv_bonus_qty,inv_tp=inv_tp,inv_amnt=inv_amnt,ret_qty=ret_qty,ret_bonus_qty=ret_bonus_qty,ret_amnt=ret_amnt,rtnP_total=rtnP_total,nsP_total=nsP_total,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,teritory_id=teritory_id,teritory_name=teritory_name,total=total,page=page,items_per_page=items_per_page)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))

def customerWiseSalesSDetailP():
    c_id=session.cid
    response.title='Customer Wise Sales Statement Detail'
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
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
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))


    qset_sum=db()
    qset_sum=qset_sum(db.sm_invoice_head.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice_head.status=='Invoiced')
    qset_sum=qset_sum((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    if (depot_id!=''):
        qset=qset(db.sm_invoice_head.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice_head.store_id==store_id)
        qset_sum=qset_sum(db.sm_invoice_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_invoice_head.client_id==customer_id)
        qset_sum=qset_sum(db.sm_invoice_head.client_id==customer_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_invoice_head.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_invoice_head.rep_id==mso_id)
    if (market_id!=''):
        qset=qset(db.sm_invoice_head.market_id==market_id)
        qset_sum=qset_sum(db.sm_invoice_head.market_id==market_id)
        
    if (teritory_id!=''):
       qset=qset(db.sm_invoice_head.area_id==teritory_id)
       qset_sum=qset_sum(db.sm_invoice_head.area_id==teritory_id)
    
    records=qset.select(db.sm_invoice_head.sl.count(),db.sm_invoice_head.depot_id,db.sm_invoice_head.client_id,db.sm_invoice_head.client_name,db.sm_invoice_head.rep_id,db.sm_invoice_head.rep_name,db.sm_invoice_head.market_id,db.sm_invoice_head.market_name,db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_sp_discount.sum(),db.sm_invoice_head.return_discount.sum(),orderby=db.sm_invoice_head.client_name,groupby=db.sm_invoice_head.client_id)
   
    
    condition_ret=''
    if (depot_id!=''):
        condition_ret=condition_ret+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition_ret=condition_ret+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition_ret=condition_ret+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition_ret=condition_ret+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition_ret=condition_ret+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition_ret=condition_ret+"AND area_id= '"+str(teritory_id)+"'"
    
    records_retS="SELECT  sum(item_vat * (quantity-return_qty)) as vat_amnt, sum(quantity) as inv_qty ,sum(bonus_qty) as inv_bonus_qty,sum(quantity * actual_tp) as inv_tp,sum(quantity * actual_tp) as inv_amnt,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty,sum(return_qty * actual_tp) as ret_amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+condition_ret+"  limit  1;"
    records_ret=db.executesql(records_retS,as_dict = True) 

    if records:
        for records_ret in records_ret:
            vat_amnt=records_ret['vat_amnt']
            inv_qty=records_ret['inv_qty']
            inv_bonus_qty=records_ret['inv_bonus_qty']
            inv_tp=records_ret['inv_tp']
            inv_amnt=records_ret['inv_amnt']
            ret_qty=records_ret['ret_qty']
            ret_bonus_qty=records_ret['ret_bonus_qty']
            ret_amnt=records_ret['ret_amnt']
            vat_amnt=records_ret['vat_amnt']
            

            rtnP_total=(ret_amnt*100)/inv_amnt
            nsP_total =((inv_amnt-ret_amnt) *100)/inv_amnt
            
            
            
            
            rtnP_total=(ret_amnt*100)/inv_amnt
            
#         return ret_amnt
        record_sum=qset_sum.select((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_discount).sum(),db.sm_invoice_head.total_amount.sum(),(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),(db.sm_invoice_head.return_discount).sum(),(db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_vat.sum(), limitby=(0,1))
#         return db._lastsql
        total=0.0
       
        
        for rec in record_sum:          
            disc=rec[db.sm_invoice_head.discount.sum()]-rec[db.sm_invoice_head.return_discount.sum()]
            spdisc=rec[db.sm_invoice_head.sp_discount.sum()]
            retdisc=rec[db.sm_invoice_head.return_sp_discount.sum()]

    
        
        qsetRet=db()
        qsetRet=qsetRet(db.sm_invoice_head.cid==c_id)
        qsetRet=qsetRet(db.sm_invoice.cid==db.sm_invoice_head.cid)
        qsetRet=qsetRet(db.sm_invoice.sl==db.sm_invoice_head.sl)
        qsetRet=qsetRet(db.sm_invoice.depot_id==db.sm_invoice_head.depot_id)
        qsetRet=qsetRet(db.sm_invoice.status=='Invoiced')
        qsetRet=qsetRet(db.sm_invoice.return_qty!=0)
        qsetRet=qsetRet((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
        
        if (depot_id!=''): 
            qsetRet=qsetRet(db.sm_invoice.depot_id==depot_id)   
        if (store_id!=''):
            qsetRet=qsetRet(db.sm_invoice.store_id==store_id)
            
        if (customer_id!=''):
            qsetRet=qsetRet(db.sm_invoice.client_id==customer_id)
         
        if (mso_id!=''):
            qsetRet=qsetRet(db.sm_invoice.rep_id==mso_id)
        if (market_id!=''):
            qsetRet=qsetRet(db.sm_invoice.market_id==market_id)
            
            

        retCountRows=qsetRet.select(db.sm_invoice.client_id,db.sm_invoice_head.sl.count(),orderby=db.sm_invoice.client_name,groupby=db.sm_invoice.client_id)
    #     return invCountRows
        
        retList=[]
        retList_str=[]
        for retCountRows in retCountRows:
            retCust_id = retCountRows[db.sm_invoice.client_id]
            retCount = retCountRows[db.sm_invoice_head.sl.count()]
            retList.append(retCust_id)
            retList_str.append(retCount)
        
            
        
        return dict(records=records,retList=retList,retList_str=retList_str,disc=disc,spdisc=spdisc,retdisc=retdisc,vat_amnt=vat_amnt,inv_qty=inv_qty,inv_bonus_qty=inv_bonus_qty,inv_tp=inv_tp,inv_amnt=inv_amnt,ret_qty=ret_qty,ret_bonus_qty=ret_bonus_qty,ret_amnt=ret_amnt,rtnP_total=rtnP_total,nsP_total=nsP_total,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,teritory_id=teritory_id,teritory_name=teritory_name,total=total,page=page,items_per_page=items_per_page)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
        
        
def customerWiseSalesSDetailPD():
    c_id=session.cid
    response.title='Customer Wise Sales Statement Detail'
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
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
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))


    qset_sum=db()
    qset_sum=qset_sum(db.sm_invoice_head.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice_head.status=='Invoiced')
    qset_sum=qset_sum((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    if (depot_id!=''):
        qset=qset(db.sm_invoice_head.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice_head.store_id==store_id)
        qset_sum=qset_sum(db.sm_invoice_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_invoice_head.client_id==customer_id)
        qset_sum=qset_sum(db.sm_invoice_head.client_id==customer_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_invoice_head.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_invoice_head.rep_id==mso_id)
    if (market_id!=''):
        qset=qset(db.sm_invoice_head.market_id==market_id)
        qset_sum=qset_sum(db.sm_invoice_head.market_id==market_id)
        
    if (teritory_id!=''):
       qset=qset(db.sm_invoice_head.area_id==teritory_id)
       qset_sum=qset_sum(db.sm_invoice_head.area_id==teritory_id)
    
    records=qset.select(db.sm_invoice_head.sl.count(),db.sm_invoice_head.depot_id,db.sm_invoice_head.client_id,db.sm_invoice_head.client_name,db.sm_invoice_head.rep_id,db.sm_invoice_head.rep_name,db.sm_invoice_head.market_id,db.sm_invoice_head.market_name,db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_sp_discount.sum(),db.sm_invoice_head.return_discount.sum(),orderby=db.sm_invoice_head.client_name,groupby=db.sm_invoice_head.client_id)
   
    
    condition_ret=''
    if (depot_id!=''):
        condition_ret=condition_ret+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition_ret=condition_ret+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition_ret=condition_ret+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition_ret=condition_ret+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition_ret=condition_ret+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition_ret=condition_ret+"AND area_id= '"+str(teritory_id)+"'"
    
    records_retS="SELECT  sum(item_vat * (quantity-return_qty)) as vat_amnt, sum(quantity) as inv_qty ,sum(bonus_qty) as inv_bonus_qty,sum(quantity * actual_tp) as inv_tp,sum(quantity * actual_tp) as inv_amnt,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty,sum(return_qty * actual_tp) as ret_amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+condition_ret+"  limit  1;"
    records_ret=db.executesql(records_retS,as_dict = True) 

    if records:
        for records_ret in records_ret:
            vat_amnt=records_ret['vat_amnt']
            inv_qty=records_ret['inv_qty']
            inv_bonus_qty=records_ret['inv_bonus_qty']
            inv_tp=records_ret['inv_tp']
            inv_amnt=records_ret['inv_amnt']
            ret_qty=records_ret['ret_qty']
            ret_bonus_qty=records_ret['ret_bonus_qty']
            ret_amnt=records_ret['ret_amnt']
            vat_amnt=records_ret['vat_amnt']
            

            rtnP_total=(ret_amnt*100)/inv_amnt
            nsP_total =((inv_amnt-ret_amnt) *100)/inv_amnt
            
            
            
            
            rtnP_total=(ret_amnt*100)/inv_amnt
            
#         return ret_amnt
        record_sum=qset_sum.select((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_discount).sum(),db.sm_invoice_head.total_amount.sum(),(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),(db.sm_invoice_head.return_discount).sum(),(db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_vat.sum(), limitby=(0,1))
#         return db._lastsql
        total=0.0
       
        
        for rec in record_sum:          
            disc=rec[db.sm_invoice_head.discount.sum()]-rec[db.sm_invoice_head.return_discount.sum()]
            spdisc=rec[db.sm_invoice_head.sp_discount.sum()]
            retdisc=rec[db.sm_invoice_head.return_sp_discount.sum()]

    
        
        qsetRet=db()
        qsetRet=qsetRet(db.sm_invoice_head.cid==c_id)
        qsetRet=qsetRet(db.sm_invoice.cid==db.sm_invoice_head.cid)
        qsetRet=qsetRet(db.sm_invoice.sl==db.sm_invoice_head.sl)
        qsetRet=qsetRet(db.sm_invoice.depot_id==db.sm_invoice_head.depot_id)
        qsetRet=qsetRet(db.sm_invoice.status=='Invoiced')
        qsetRet=qsetRet(db.sm_invoice.return_qty!=0)
        qsetRet=qsetRet((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
        
        if (depot_id!=''): 
            qsetRet=qsetRet(db.sm_invoice.depot_id==depot_id)   
        if (store_id!=''):
            qsetRet=qsetRet(db.sm_invoice.store_id==store_id)
            
        if (customer_id!=''):
            qsetRet=qsetRet(db.sm_invoice.client_id==customer_id)
         
        if (mso_id!=''):
            qsetRet=qsetRet(db.sm_invoice.rep_id==mso_id)
        if (market_id!=''):
            qsetRet=qsetRet(db.sm_invoice.market_id==market_id)
            
            

        retCountRows=qsetRet.select(db.sm_invoice.client_id,db.sm_invoice_head.sl.count(),orderby=db.sm_invoice.client_name,groupby=db.sm_invoice.client_id)
    #     return invCountRows
        
        retList=[]
        retList_str=[]
        for retCountRows in retCountRows:
            retCust_id = retCountRows[db.sm_invoice.client_id]
            retCount = retCountRows[db.sm_invoice_head.sl.count()]
            retList.append(retCust_id)
            retList_str.append(retCount)
        
            
    if records:
        myString='Customer Information\n'
        myString=myString+'DateRange,'+date_from+'|'+date_to+'\n'
        myString=myString+'Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString=myString+'Store,'+store_id+'|'+store_name+'\n'
        myString=myString+'Customer,'+customer_id+'|'+customer_name+'\n'
        myString=myString+'Teritory,'+teritory_id+'|'+teritory_name+'\n\n'
        myString=myString+'MSO,'+mso_id+'|'+mso_name+'\n\n'
         
       
         
        myString+='CustomerID,CustomerName  ,  MSO  ,  Market  ,  InvCount  ,  RetCount  ,  InvTP  ,  RetTP  ,  NetTP  ,  NetDisc  ,  NetVat ,   Net\n'
          
        for record in records: 
            custRet=0
            client_id=record[db.sm_invoice_head.client_id]
            if [s for s in retList if client_id in s]:
                ret_index_element = retList.index(client_id)           
                custRet=retList_str[ret_index_element]
            retNet=record[db.sm_invoice_head.return_tp.sum()]+record[db.sm_invoice_head.return_vat.sum()]-(record[db.sm_invoice_head.return_sp_discount.sum()]+record[db.sm_invoice_head.return_discount.sum()])
            
            myString=myString+str(record[db.sm_invoice_head.client_id])+','+str(record[db.sm_invoice_head.client_name])+','+str(record[db.sm_invoice_head.sl.count()])+','+str(custRet)+','+str(record[db.sm_invoice_head.actual_total_tp.sum()])+','+str(record[db.sm_invoice_head.return_tp.sum()])+','+str(record[db.sm_invoice_head.actual_total_tp.sum()]-record[db.sm_invoice_head.return_tp.sum()])+','+str((record[db.sm_invoice_head.discount.sum()]+record[db.sm_invoice_head.sp_discount.sum()])-(record[db.sm_invoice_head.return_sp_discount.sum()]+record[db.sm_invoice_head.return_discount.sum()]))+','+str(record[db.sm_invoice_head.vat_total_amount.sum()]-record[db.sm_invoice_head.return_vat.sum()])+','+str(record[db.sm_invoice_head.total_amount.sum()]-retNet)+'\n'
         
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=CustWiseSalesStatementDetail.csv'   
        return str(myString)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
# ---------------------------------------------------------------
def msoWiseSalesSDetail():
    c_id=session.cid
    response.title='Customer Wise Sales Statement Detail'
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
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
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))


    qset_sum=db()
    qset_sum=qset_sum(db.sm_invoice_head.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice_head.status=='Invoiced')
    qset_sum=qset_sum((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    if (depot_id!=''):
        qset=qset(db.sm_invoice_head.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice_head.store_id==store_id)
        qset_sum=qset_sum(db.sm_invoice_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_invoice_head.client_id==customer_id)
        qset_sum=qset_sum(db.sm_invoice_head.client_id==customer_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_invoice_head.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_invoice_head.rep_id==mso_id)
    if (market_id!=''):
        qset=qset(db.sm_invoice_head.market_id==market_id)
        qset_sum=qset_sum(db.sm_invoice_head.market_id==market_id)
        
    if (teritory_id!=''):
       qset=qset(db.sm_invoice_head.area_id==teritory_id)
       qset_sum=qset_sum(db.sm_invoice_head.area_id==teritory_id)
    
    records=qset.select(db.sm_invoice_head.sl.count(),db.sm_invoice_head.depot_id,db.sm_invoice_head.rep_id,db.sm_invoice_head.rep_name,db.sm_invoice_head.rep_id,db.sm_invoice_head.rep_name,db.sm_invoice_head.market_id,db.sm_invoice_head.market_name,db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_sp_discount.sum(),db.sm_invoice_head.return_discount.sum(),orderby=db.sm_invoice_head.rep_name,groupby=db.sm_invoice_head.rep_id)
   
    
    condition_ret=''
    if (depot_id!=''):
        condition_ret=condition_ret+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition_ret=condition_ret+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition_ret=condition_ret+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition_ret=condition_ret+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition_ret=condition_ret+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition_ret=condition_ret+"AND area_id= '"+str(teritory_id)+"'"
    
    records_retS="SELECT  sum(item_vat * (quantity-return_qty)) as vat_amnt, sum(quantity) as inv_qty ,sum(bonus_qty) as inv_bonus_qty,sum(quantity * actual_tp) as inv_tp,sum(quantity * actual_tp) as inv_amnt,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty,sum(return_qty * actual_tp) as ret_amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+condition_ret+"  limit  1;"
    records_ret=db.executesql(records_retS,as_dict = True) 

    if records:
        for records_ret in records_ret:
            vat_amnt=records_ret['vat_amnt']
            inv_qty=records_ret['inv_qty']
            inv_bonus_qty=records_ret['inv_bonus_qty']
            inv_tp=records_ret['inv_tp']
            inv_amnt=records_ret['inv_amnt']
            ret_qty=records_ret['ret_qty']
            ret_bonus_qty=records_ret['ret_bonus_qty']
            ret_amnt=records_ret['ret_amnt']
            vat_amnt=records_ret['vat_amnt']
            

            rtnP_total=(ret_amnt*100)/inv_amnt
            nsP_total =((inv_amnt-ret_amnt) *100)/inv_amnt
            
            
            
            
            rtnP_total=(ret_amnt*100)/inv_amnt
            
#         return ret_amnt
        record_sum=qset_sum.select((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_discount).sum(),db.sm_invoice_head.total_amount.sum(),(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),(db.sm_invoice_head.return_discount).sum(),(db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_vat.sum(), limitby=(0,1))
#         return db._lastsql
        total=0.0
       
        
        for rec in record_sum:          
            disc=rec[db.sm_invoice_head.discount.sum()]-rec[db.sm_invoice_head.return_discount.sum()]
            spdisc=rec[db.sm_invoice_head.sp_discount.sum()]
            retdisc=rec[db.sm_invoice_head.return_sp_discount.sum()]

    
        
        qsetRet=db()
        qsetRet=qsetRet(db.sm_invoice_head.cid==c_id)
        qsetRet=qsetRet(db.sm_invoice.cid==db.sm_invoice_head.cid)
        qsetRet=qsetRet(db.sm_invoice.sl==db.sm_invoice_head.sl)
        qsetRet=qsetRet(db.sm_invoice.depot_id==db.sm_invoice_head.depot_id)
        qsetRet=qsetRet(db.sm_invoice.status=='Invoiced')
        qsetRet=qsetRet(db.sm_invoice.return_qty!=0)
        qsetRet=qsetRet((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
        
        if (depot_id!=''): 
            qsetRet=qsetRet(db.sm_invoice.depot_id==depot_id)   
        if (store_id!=''):
            qsetRet=qsetRet(db.sm_invoice.store_id==store_id)
            
        if (customer_id!=''):
            qsetRet=qsetRet(db.sm_invoice.client_id==customer_id)
         
        if (mso_id!=''):
            qsetRet=qsetRet(db.sm_invoice.rep_id==mso_id)
        if (market_id!=''):
            qsetRet=qsetRet(db.sm_invoice.market_id==market_id)
            
            

        retCountRows=qsetRet.select(db.sm_invoice.rep_id,db.sm_invoice_head.sl.count(),orderby=db.sm_invoice.rep_name,groupby=db.sm_invoice.rep_id)
    #     return invCountRows
        
        retList=[]
        retList_str=[]
        for retCountRows in retCountRows:
            retRep_id = retCountRows[db.sm_invoice.rep_id]
            retCount = retCountRows[db.sm_invoice_head.sl.count()]
            retList.append(retRep_id)
            retList_str.append(retCount)
        
            
        
        return dict(records=records,retList=retList,retList_str=retList_str,disc=disc,spdisc=spdisc,retdisc=retdisc,vat_amnt=vat_amnt,inv_qty=inv_qty,inv_bonus_qty=inv_bonus_qty,inv_tp=inv_tp,inv_amnt=inv_amnt,ret_qty=ret_qty,ret_bonus_qty=ret_bonus_qty,ret_amnt=ret_amnt,rtnP_total=rtnP_total,nsP_total=nsP_total,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,teritory_id=teritory_id,teritory_name=teritory_name,total=total,page=page,items_per_page=items_per_page)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))  
        
def msoWiseSalesSDetailD():
    c_id=session.cid
    response.title='MSO Wise Sales Statement Detail'
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
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
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))


    qset_sum=db()
    qset_sum=qset_sum(db.sm_invoice_head.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice_head.status=='Invoiced')
    qset_sum=qset_sum((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    if (depot_id!=''):
        qset=qset(db.sm_invoice_head.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice_head.store_id==store_id)
        qset_sum=qset_sum(db.sm_invoice_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_invoice_head.client_id==customer_id)
        qset_sum=qset_sum(db.sm_invoice_head.client_id==customer_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_invoice_head.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_invoice_head.rep_id==mso_id)
    if (market_id!=''):
        qset=qset(db.sm_invoice_head.market_id==market_id)
        qset_sum=qset_sum(db.sm_invoice_head.market_id==market_id)
        
    if (teritory_id!=''):
       qset=qset(db.sm_invoice_head.area_id==teritory_id)
       qset_sum=qset_sum(db.sm_invoice_head.area_id==teritory_id)
    
    records=qset.select(db.sm_invoice_head.sl.count(),db.sm_invoice_head.depot_id,db.sm_invoice_head.rep_id,db.sm_invoice_head.rep_name,db.sm_invoice_head.rep_id,db.sm_invoice_head.rep_name,db.sm_invoice_head.market_id,db.sm_invoice_head.market_name,db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_sp_discount.sum(),db.sm_invoice_head.return_discount.sum(),orderby=db.sm_invoice_head.rep_name,groupby=db.sm_invoice_head.rep_id)
   
    
    condition_ret=''
    if (depot_id!=''):
        condition_ret=condition_ret+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition_ret=condition_ret+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition_ret=condition_ret+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition_ret=condition_ret+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition_ret=condition_ret+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition_ret=condition_ret+"AND area_id= '"+str(teritory_id)+"'"
    
    records_retS="SELECT  sum(item_vat * (quantity-return_qty)) as vat_amnt, sum(quantity) as inv_qty ,sum(bonus_qty) as inv_bonus_qty,sum(quantity * actual_tp) as inv_tp,sum(quantity * actual_tp) as inv_amnt,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty,sum(return_qty * actual_tp) as ret_amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+condition_ret+"  limit  1;"
    records_ret=db.executesql(records_retS,as_dict = True) 

    if records:
        for records_ret in records_ret:
            vat_amnt=records_ret['vat_amnt']
            inv_qty=records_ret['inv_qty']
            inv_bonus_qty=records_ret['inv_bonus_qty']
            inv_tp=records_ret['inv_tp']
            inv_amnt=records_ret['inv_amnt']
            ret_qty=records_ret['ret_qty']
            ret_bonus_qty=records_ret['ret_bonus_qty']
            ret_amnt=records_ret['ret_amnt']
            vat_amnt=records_ret['vat_amnt']
            

            rtnP_total=(ret_amnt*100)/inv_amnt
            nsP_total =((inv_amnt-ret_amnt) *100)/inv_amnt
            
            
            
            
            rtnP_total=(ret_amnt*100)/inv_amnt
            
#         return ret_amnt
        record_sum=qset_sum.select((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_discount).sum(),db.sm_invoice_head.total_amount.sum(),(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),(db.sm_invoice_head.return_discount).sum(),(db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_vat.sum(), limitby=(0,1))
#         return db._lastsql
        total=0.0
       
        
        for rec in record_sum:          
            disc=rec[db.sm_invoice_head.discount.sum()]-rec[db.sm_invoice_head.return_discount.sum()]
            spdisc=rec[db.sm_invoice_head.sp_discount.sum()]
            retdisc=rec[db.sm_invoice_head.return_sp_discount.sum()]

    
        
        qsetRet=db()
        qsetRet=qsetRet(db.sm_invoice_head.cid==c_id)
        qsetRet=qsetRet(db.sm_invoice.cid==db.sm_invoice_head.cid)
        qsetRet=qsetRet(db.sm_invoice.sl==db.sm_invoice_head.sl)
        qsetRet=qsetRet(db.sm_invoice.depot_id==db.sm_invoice_head.depot_id)
        qsetRet=qsetRet(db.sm_invoice.status=='Invoiced')
        qsetRet=qsetRet(db.sm_invoice.return_qty!=0)
        qsetRet=qsetRet((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
        
        if (depot_id!=''): 
            qsetRet=qsetRet(db.sm_invoice.depot_id==depot_id)   
        if (store_id!=''):
            qsetRet=qsetRet(db.sm_invoice.store_id==store_id)
            
        if (customer_id!=''):
            qsetRet=qsetRet(db.sm_invoice.client_id==customer_id)
         
        if (mso_id!=''):
            qsetRet=qsetRet(db.sm_invoice.rep_id==mso_id)
        if (market_id!=''):
            qsetRet=qsetRet(db.sm_invoice.market_id==market_id)
            
            

        retCountRows=qsetRet.select(db.sm_invoice.rep_id,db.sm_invoice_head.sl.count(),orderby=db.sm_invoice.rep_name,groupby=db.sm_invoice.rep_id)
    #     return invCountRows
        
        retList=[]
        retList_str=[]
        for retCountRows in retCountRows:
            retRep_id = retCountRows[db.sm_invoice.rep_id]
            retCount = retCountRows[db.sm_invoice_head.sl.count()]
            retList.append(retRep_id)
            retList_str.append(retCount)
        
            
    if records:
        
     
        myString='MSO WiseSales StatementDetail\n'
        myString=myString+'DateRange,'+date_from+'|'+date_to+'\n'
        myString=myString+'Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString=myString+'Store,'+store_id+'|'+store_name+'\n'
        myString=myString+'Customer,'+customer_id+'|'+customer_name+'\n'
        myString=myString+'Teritory,'+teritory_id+'|'+teritory_name+'\n\n'
        myString=myString+'MSO,'+mso_id+'|'+mso_name+'\n\n'
         
       
         
        myString+='MSOID,MsoName  ,  InvCount  ,  RetCount  ,  InvTP    RetTP    NetTP    Disc    Vat    Net\n'
          
        for record in records: 
            repRet=0
            rep_id=record[db.sm_invoice_head.rep_id]
            if [s for s in retList if rep_id in s]:
                ret_index_element = retList.index(rep_id)           
                repRet=retList_str[ret_index_element]
            retNet=record[db.sm_invoice_head.return_tp.sum()]+record[db.sm_invoice_head.return_vat.sum()]-(record[db.sm_invoice_head.return_sp_discount.sum()]+record[db.sm_invoice_head.return_discount.sum()])
            
            myString=myString+str(record[db.sm_invoice_head.rep_id])+','+str(record[db.sm_invoice_head.rep_name])+','+str(record[db.sm_invoice_head.sl.count()])+','+str(repRet)+','+str(record[db.sm_invoice_head.actual_total_tp.sum()])+','+str(record[db.sm_invoice_head.return_tp.sum()])+','+str(record[db.sm_invoice_head.actual_total_tp.sum()]-record[db.sm_invoice_head.return_tp.sum()])+','+str((record[db.sm_invoice_head.discount.sum()]+record[db.sm_invoice_head.sp_discount.sum()])-(record[db.sm_invoice_head.return_sp_discount.sum()]+record[db.sm_invoice_head.return_discount.sum()]))+','+str(record[db.sm_invoice_head.vat_total_amount.sum()]-record[db.sm_invoice_head.return_vat.sum()])+','+str(record[db.sm_invoice_head.total_amount.sum()]-retNet)+'\n'
         
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=MSOWiseSalesStatementDetail.csv'   
        return str(myString)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))          
        
        
        
# ----------------------------------------------------------------        
              
def dpWiseSalesSDetail():
    c_id=session.cid
    response.title='Customer Wise Sales Statement Detail'
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
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
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))


    qset_sum=db()
    qset_sum=qset_sum(db.sm_invoice_head.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice_head.status=='Invoiced')
    qset_sum=qset_sum((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    if (depot_id!=''):
        qset=qset(db.sm_invoice_head.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice_head.store_id==store_id)
        qset_sum=qset_sum(db.sm_invoice_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_invoice_head.client_id==customer_id)
        qset_sum=qset_sum(db.sm_invoice_head.client_id==customer_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_invoice_head.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_invoice_head.rep_id==mso_id)
    if (market_id!=''):
        qset=qset(db.sm_invoice_head.market_id==market_id)
        qset_sum=qset_sum(db.sm_invoice_head.market_id==market_id)
        
    if (teritory_id!=''):
       qset=qset(db.sm_invoice_head.area_id==teritory_id)
       qset_sum=qset_sum(db.sm_invoice_head.area_id==teritory_id)
    
    records=qset.select(db.sm_invoice_head.sl.count(),db.sm_invoice_head.depot_id,db.sm_invoice_head.d_man_id,db.sm_invoice_head.d_man_name,db.sm_invoice_head.rep_id,db.sm_invoice_head.rep_name,db.sm_invoice_head.rep_id,db.sm_invoice_head.rep_name,db.sm_invoice_head.market_id,db.sm_invoice_head.market_name,db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_sp_discount.sum(),db.sm_invoice_head.return_discount.sum(),orderby=db.sm_invoice_head.d_man_name,groupby=db.sm_invoice_head.d_man_id)
#     return records
    
    condition_ret=''
    if (depot_id!=''):
        condition_ret=condition_ret+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition_ret=condition_ret+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition_ret=condition_ret+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition_ret=condition_ret+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition_ret=condition_ret+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition_ret=condition_ret+"AND area_id= '"+str(teritory_id)+"'"
    
    records_retS="SELECT  sum(item_vat * (quantity-return_qty)) as vat_amnt, sum(quantity) as inv_qty ,sum(bonus_qty) as inv_bonus_qty,sum(quantity * actual_tp) as inv_tp,sum(quantity * actual_tp) as inv_amnt,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty,sum(return_qty * actual_tp) as ret_amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+condition_ret+"  limit  1;"
    records_ret=db.executesql(records_retS,as_dict = True) 

    if records:
        for records_ret in records_ret:
            vat_amnt=records_ret['vat_amnt']
            inv_qty=records_ret['inv_qty']
            inv_bonus_qty=records_ret['inv_bonus_qty']
            inv_tp=records_ret['inv_tp']
            inv_amnt=records_ret['inv_amnt']
            ret_qty=records_ret['ret_qty']
            ret_bonus_qty=records_ret['ret_bonus_qty']
            ret_amnt=records_ret['ret_amnt']
            vat_amnt=records_ret['vat_amnt']
            

            rtnP_total=(ret_amnt*100)/inv_amnt
            nsP_total =((inv_amnt-ret_amnt) *100)/inv_amnt
            
            
            
            
            rtnP_total=(ret_amnt*100)/inv_amnt
            
#         return ret_amnt
        record_sum=qset_sum.select((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_discount).sum(),db.sm_invoice_head.total_amount.sum(),(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),(db.sm_invoice_head.return_discount).sum(),(db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_vat.sum(), limitby=(0,1))
#         return db._lastsql
        total=0.0
       
        
        for rec in record_sum:          
            disc=rec[db.sm_invoice_head.discount.sum()]-rec[db.sm_invoice_head.return_discount.sum()]
            spdisc=rec[db.sm_invoice_head.sp_discount.sum()]
            retdisc=rec[db.sm_invoice_head.return_sp_discount.sum()]

    
        
        qsetRet=db()
        qsetRet=qsetRet(db.sm_invoice_head.cid==c_id)
        qsetRet=qsetRet(db.sm_invoice.cid==db.sm_invoice_head.cid)
        qsetRet=qsetRet(db.sm_invoice.sl==db.sm_invoice_head.sl)
        qsetRet=qsetRet(db.sm_invoice.depot_id==db.sm_invoice_head.depot_id)
        qsetRet=qsetRet(db.sm_invoice.status=='Invoiced')
        qsetRet=qsetRet(db.sm_invoice.return_qty!=0)
        qsetRet=qsetRet((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
        
        if (depot_id!=''): 
            qsetRet=qsetRet(db.sm_invoice.depot_id==depot_id)   
        if (store_id!=''):
            qsetRet=qsetRet(db.sm_invoice.store_id==store_id)
            
        if (customer_id!=''):
            qsetRet=qsetRet(db.sm_invoice.client_id==customer_id)
         
        if (mso_id!=''):
            qsetRet=qsetRet(db.sm_invoice.rep_id==mso_id)
        if (market_id!=''):
            qsetRet=qsetRet(db.sm_invoice.market_id==market_id)
            
            

        retCountRows=qsetRet.select(db.sm_invoice.d_man_id,db.sm_invoice_head.sl.count(),orderby=db.sm_invoice.d_man_name,groupby=db.sm_invoice.d_man_id)
    #     return invCountRows
        
        retList=[]
        retList_str=[]
        for retCountRows in retCountRows:
            dman_id = retCountRows[db.sm_invoice.d_man_id]
            retCount = retCountRows[db.sm_invoice_head.sl.count()]
            retList.append(dman_id)
            retList_str.append(retCount)
        
            
        
        return dict(records=records,retList=retList,retList_str=retList_str,disc=disc,spdisc=spdisc,retdisc=retdisc,vat_amnt=vat_amnt,inv_qty=inv_qty,inv_bonus_qty=inv_bonus_qty,inv_tp=inv_tp,inv_amnt=inv_amnt,ret_qty=ret_qty,ret_bonus_qty=ret_bonus_qty,ret_amnt=ret_amnt,rtnP_total=rtnP_total,nsP_total=nsP_total,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,teritory_id=teritory_id,teritory_name=teritory_name,total=total,page=page,items_per_page=items_per_page)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))   
        


def dpWiseSalesSDetailD():
    c_id=session.cid
    response.title='Delivery Person Wise Sales Statement Detail'
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
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
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))


    qset_sum=db()
    qset_sum=qset_sum(db.sm_invoice_head.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice_head.status=='Invoiced')
    qset_sum=qset_sum((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    if (depot_id!=''):
        qset=qset(db.sm_invoice_head.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice_head.store_id==store_id)
        qset_sum=qset_sum(db.sm_invoice_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_invoice_head.client_id==customer_id)
        qset_sum=qset_sum(db.sm_invoice_head.client_id==customer_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_invoice_head.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_invoice_head.rep_id==mso_id)
    if (market_id!=''):
        qset=qset(db.sm_invoice_head.market_id==market_id)
        qset_sum=qset_sum(db.sm_invoice_head.market_id==market_id)
        
    if (teritory_id!=''):
       qset=qset(db.sm_invoice_head.area_id==teritory_id)
       qset_sum=qset_sum(db.sm_invoice_head.area_id==teritory_id)
    
    records=qset.select(db.sm_invoice_head.sl.count(),db.sm_invoice_head.depot_id,db.sm_invoice_head.d_man_id,db.sm_invoice_head.d_man_name,db.sm_invoice_head.rep_id,db.sm_invoice_head.rep_name,db.sm_invoice_head.rep_id,db.sm_invoice_head.rep_name,db.sm_invoice_head.market_id,db.sm_invoice_head.market_name,db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_sp_discount.sum(),db.sm_invoice_head.return_discount.sum(),orderby=db.sm_invoice_head.d_man_name,groupby=db.sm_invoice_head.d_man_id)
#     return records
    
    condition_ret=''
    if (depot_id!=''):
        condition_ret=condition_ret+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition_ret=condition_ret+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition_ret=condition_ret+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition_ret=condition_ret+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition_ret=condition_ret+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition_ret=condition_ret+"AND area_id= '"+str(teritory_id)+"'"
    
    records_retS="SELECT  sum(item_vat * (quantity-return_qty)) as vat_amnt, sum(quantity) as inv_qty ,sum(bonus_qty) as inv_bonus_qty,sum(quantity * actual_tp) as inv_tp,sum(quantity * actual_tp) as inv_amnt,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty,sum(return_qty * actual_tp) as ret_amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+condition_ret+"  limit  1;"
    records_ret=db.executesql(records_retS,as_dict = True) 

    if records:
        for records_ret in records_ret:
            vat_amnt=records_ret['vat_amnt']
            inv_qty=records_ret['inv_qty']
            inv_bonus_qty=records_ret['inv_bonus_qty']
            inv_tp=records_ret['inv_tp']
            inv_amnt=records_ret['inv_amnt']
            ret_qty=records_ret['ret_qty']
            ret_bonus_qty=records_ret['ret_bonus_qty']
            ret_amnt=records_ret['ret_amnt']
            vat_amnt=records_ret['vat_amnt']
            

            rtnP_total=(ret_amnt*100)/inv_amnt
            nsP_total =((inv_amnt-ret_amnt) *100)/inv_amnt
            
            
            
            
            rtnP_total=(ret_amnt*100)/inv_amnt
            
#         return ret_amnt
        record_sum=qset_sum.select((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_discount).sum(),db.sm_invoice_head.total_amount.sum(),(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),(db.sm_invoice_head.return_discount).sum(),(db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_vat.sum(), limitby=(0,1))
#         return db._lastsql
        total=0.0
       
        
        for rec in record_sum:          
            disc=rec[db.sm_invoice_head.discount.sum()]-rec[db.sm_invoice_head.return_discount.sum()]
            spdisc=rec[db.sm_invoice_head.sp_discount.sum()]
            retdisc=rec[db.sm_invoice_head.return_sp_discount.sum()]

    
        
        qsetRet=db()
        qsetRet=qsetRet(db.sm_invoice_head.cid==c_id)
        qsetRet=qsetRet(db.sm_invoice.cid==db.sm_invoice_head.cid)
        qsetRet=qsetRet(db.sm_invoice.sl==db.sm_invoice_head.sl)
        qsetRet=qsetRet(db.sm_invoice.depot_id==db.sm_invoice_head.depot_id)
        qsetRet=qsetRet(db.sm_invoice.status=='Invoiced')
        qsetRet=qsetRet(db.sm_invoice.return_qty!=0)
        qsetRet=qsetRet((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
        
        if (depot_id!=''): 
            qsetRet=qsetRet(db.sm_invoice.depot_id==depot_id)   
        if (store_id!=''):
            qsetRet=qsetRet(db.sm_invoice.store_id==store_id)
            
        if (customer_id!=''):
            qsetRet=qsetRet(db.sm_invoice.client_id==customer_id)
         
        if (mso_id!=''):
            qsetRet=qsetRet(db.sm_invoice.rep_id==mso_id)
        if (market_id!=''):
            qsetRet=qsetRet(db.sm_invoice.market_id==market_id)
            
            

        retCountRows=qsetRet.select(db.sm_invoice.d_man_id,db.sm_invoice_head.sl.count(),orderby=db.sm_invoice.d_man_name,groupby=db.sm_invoice.d_man_id)
    #     return invCountRows
        
        retList=[]
        retList_str=[]
        for retCountRows in retCountRows:
            dman_id = retCountRows[db.sm_invoice.d_man_id]
            retCount = retCountRows[db.sm_invoice_head.sl.count()]
            retList.append(dman_id)
            retList_str.append(retCount)
             
             
         
    if records:
        
     
        myString='Delivery Person Wise Sales Statement Detail\n'
        myString=myString+'DateRange,'+date_from+'|'+date_to+'\n'
        myString=myString+'Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString=myString+'Store,'+store_id+'|'+store_name+'\n'
        myString=myString+'Customer,'+customer_id+'|'+customer_name+'\n'
        myString=myString+'Teritory,'+teritory_id+'|'+teritory_name+'\n\n'
        myString=myString+'MSO,'+mso_id+'|'+mso_name+'\n\n'
         
       
         
        myString+='DeliveryManID, DeliveryManName   , InvCount  ,  RetCount  ,  InvCount  ,  RetCount  ,  InvTP  ,  InvDisc  ,  InvVat  ,  InvNet  ,  RetTP  ,  RetDisc  ,  RetVat  ,  RetNet  ,  NetTP  ,  NetDisc  ,  NetVat  ,  Net\n'
          
        for record in records: 
            repRet=0
            d_man_id=record[db.sm_invoice_head.d_man_id]
            if [s for s in retList if d_man_id in s]:
                ret_index_element = retList.index(d_man_id)           
                repRet=retList_str[ret_index_element]
            retNet=record[db.sm_invoice_head.return_tp.sum()]+record[db.sm_invoice_head.return_vat.sum()]-(record[db.sm_invoice_head.return_sp_discount.sum()]+record[db.sm_invoice_head.return_discount.sum()])
            
            myString=myString+str(record[db.sm_invoice_head.d_man_id])+','+str(record[db.sm_invoice_head.d_man_name])+','+str(record[db.sm_invoice_head.sl.count()])+','+str(repRet)+','+str(record[db.sm_invoice_head.actual_total_tp.sum()])+','+str(record[db.sm_invoice_head.discount.sum()]+record[db.sm_invoice_head.sp_discount.sum()])+','+str(record[db.sm_invoice_head.vat_total_amount.sum()])+','+str(record[db.sm_invoice_head.total_amount.sum()])+','+str(record[db.sm_invoice_head.return_tp.sum()])+','+str(record[db.sm_invoice_head.return_sp_discount.sum()]+record[db.sm_invoice_head.return_discount.sum()])+','+str(record[db.sm_invoice_head.return_vat.sum()])+','+str(retNet)+','+str(record[db.sm_invoice_head.actual_total_tp.sum()]-record[db.sm_invoice_head.return_tp.sum()])+','+str((record[db.sm_invoice_head.discount.sum()]+record[db.sm_invoice_head.sp_discount.sum()])-(record[db.sm_invoice_head.return_sp_discount.sum()]+record[db.sm_invoice_head.return_discount.sum()]))+','+str(record[db.sm_invoice_head.vat_total_amount.sum()]-record[db.sm_invoice_head.return_vat.sum()])+','+str(record[db.sm_invoice_head.total_amount.sum()]-retNet)+'\n'
         
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=DPWiseSalesStatementDetail.csv'   
        return str(myString) 
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
                 
# ---------------------------------
def customrInformation():
    
    c_id=session.cid
    
    response.title='Customer Information'
    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
#     if (teritory_id==''):
#         session.flash="Please select a teritory"
#         redirect(URL(c='report_sales',f='home'))
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    qset=db()
    qset=qset(db.sm_client.cid==c_id)
    qset=qset(db.sm_rep_area.cid==c_id)
    qset=qset(db.sm_rep_area.area_id==db.sm_client.area_id)

    
    qset_sum=db()
    qset_sum=qset_sum(db.sm_client.cid==c_id)
    qset_sum=qset(db.sm_rep_area.area_id==db.sm_client.area_id)
    
    if (depot_id!=''):
        qset=qset(db.sm_client.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_client.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_client.store_id==store_id)
        qset_sum=qset_sum(db.sm_client.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_client.client_id==customer_id)
        qset_sum=qset_sum(db.sm_client.client_id==customer_id)
     
    if (teritory_id!=''):
        qset=qset(db.sm_client.area_id==teritory_id)
        qset_sum=qset_sum(db.sm_client.area_id==teritory_id)
    if (mso_id!=''):
        qset=qset(db.sm_rep_area.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_rep_area.rep_id==mso_id)
    if (market_id!=''):
        qset=qset(db.sm_client.market_id==market_id)
        qset_sum=qset_sum(db.sm_client.market_id==market_id)
        
  
    records=qset.select(db.sm_client.ALL,db.sm_rep_area.ALL,orderby=db.sm_client.client_id)
    if records:
        record_sum=qset_sum.select(db.sm_client.id.count())
    #     return record_sum
        total=0.0
        
        for rec in record_sum:
            customer_count=rec[db.sm_client.id.count()]
    
    
    
        
        
        return dict(records=records,customer_count=customer_count,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  teritory_id=teritory_id, teritory_name=teritory_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,total=total,page=page,items_per_page=items_per_page)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
        
        
def customrInformationDownload():
    
    c_id=session.cid
    
    response.title='Customer Information'
    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    qset=db()
    qset=qset(db.sm_client.cid==c_id)
    qset=qset(db.sm_rep_area.cid==c_id)
    qset=qset(db.sm_rep_area.area_id==db.sm_client.area_id)

    
    qset_sum=db()
    qset_sum=qset_sum(db.sm_client.cid==c_id)
    qset_sum=qset(db.sm_rep_area.area_id==db.sm_client.area_id)
    
    if (depot_id!=''):
        qset=qset(db.sm_client.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_client.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_client.store_id==store_id)
        qset_sum=qset_sum(db.sm_client.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_client.client_id==customer_id)
        qset_sum=qset_sum(db.sm_client.client_id==customer_id)
     
    if (teritory_id!=''):
        qset=qset(db.sm_client.area_id==teritory_id)
        qset_sum=qset_sum(db.sm_client.area_id==teritory_id) 
    if (mso_id!=''):
        qset=qset(db.sm_rep_area.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_rep_area.rep_id==mso_id)
        
  
    records=qset.select(db.sm_client.ALL,db.sm_rep_area.ALL,orderby=db.sm_client.client_id)
    if records:
        record_sum=qset_sum.select(db.sm_client.id.count())
    #     return record_sum
        total=0.0
        
        for rec in record_sum:
            customer_count=rec[db.sm_client.id.count()]
    
        myString='Customer Information\n'
        myString=myString+'Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString=myString+'Store,'+store_id+'|'+store_name+'\n'
        myString=myString+'Customer,'+customer_id+'|'+customer_name+'\n'
        myString=myString+'Teritory,'+teritory_id+'|'+teritory_name+'\n\n'
        myString=myString+'MSO,'+mso_id+'|'+mso_name+'\n\n'
        
        myString=myString+'Total,'+str(customer_count)+'\n\n\n'
        
        myString+='CustID,CustName,CustAddress,Teritory, TeritoryName,MarketID,MarketName,MSO TR,MSO Name\n'
         
        for records in records:
            CustID=str(records[db.sm_client.client_id]).replace(',','')
            CustName=str(records[db.sm_client.name]).replace(',','')
            CustAddress=str(records[db.sm_client.address]).replace(',','')
            Teritory=str(records[db.sm_client.area_id]).replace(',','')
            TeritoryName=str(records[db.sm_rep_area.area_name]).replace(',','')
            MarketID=str(records[db.sm_client.market_id]).replace(',','')
            MarketName=str(records[db.sm_client.market_name]).replace(',','')
            MSOTR=str(records[db.sm_rep_area.rep_id]).replace(',','')
            MSOName=str(records[db.sm_rep_area.rep_name]).replace(',','')
            
            myString+=str(CustID)+','+str(CustName)+','+str(CustAddress)+','+str(Teritory)+','+str(TeritoryName)+','+str(MarketID)+','+str(MarketName)+','+str(MSOTR)+','+str(MSOName)+'\n'
        
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=customerInformation.csv'   
        return str(myString) 
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
        
#      btn_MSOwiseS   

def msowiseS():
    c_id=session.cid
    
    response.title='MSO wise Sales'
    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 

    
    levelRows = db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == teritory_id)).select(db.sm_level.level1,db.sm_level.level2,limitby=(0,1))
#     return levelRows
    if levelRows:
        rsm=levelRows[0].level1
        fm=levelRows[0].level2
#     return fm
    
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)

    qset=qset(db.sm_invoice_head.status=='Invoiced')    
    qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    qset_rsm=db()
    qset_rsm=qset_rsm(db.sm_invoice_head.cid==c_id)
    qset_rsm=qset_rsm(db.sm_invoice_head.status=='Invoiced')  
    qset_rsm=qset_rsm((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    qset_fm=db()
    qset_fm=qset_fm(db.sm_invoice_head.cid==c_id)
#     qset=qset(db.sm_client.cid==c_id)
#     qset=qset(db.sm_client.client_id==db.sm_invoice.client_id)
    qset_fm=qset_fm(db.sm_invoice_head.status=='Invoiced')  
    qset_fm=qset_fm((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    
    qset_total=db()
    qset_total=qset_total(db.sm_invoice_head.cid==c_id)

    qset_total=qset_total(db.sm_invoice_head.status=='Invoiced')  
    qset_total=qset_total((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    if (depot_id!=''):
        qset=qset(db.sm_invoice_head.depot_id==depot_id)
        qset_fm=qset_fm(db.sm_invoice_head.depot_id==depot_id)
        qset_rsm=qset_rsm(db.sm_invoice_head.depot_id==depot_id)
        qset_total=qset_total(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice_head.store_id==store_id)
        qset_fm=qset_fm(db.sm_invoice_head.store_id==store_id)
        qset_rsm=qset_rsm(db.sm_invoice_head.store_id==store_id)
        qset_total=qset_total(db.sm_invoice_head.store_id==store_id)
        
    if (customer_id!=''):
        qset=qset(db.sm_invoice_head.client_id==customer_id)
        qset_fm=qset_fm(db.sm_invoice_head.client_id==customer_id)
        qset_rsm=qset_rsm(db.sm_invoice_head.client_id==customer_id)
        qset_total=qset_total(db.sm_invoice_head.client_id==customer_id)
    
    if (teritory_id!=''):
        qset=qset(db.sm_invoice_head.area_id==teritory_id)
        
        qset_rsm=qset_rsm(db.sm_invoice_head.level1_id==rsm)
        qset_fm=qset_fm(db.sm_invoice_head.level2_id==fm)
        qset_total=qset_total(db.sm_invoice_head.area_id==teritory_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_invoice_head.rep_id==mso_id)
        qset_fm=qset_fm(db.sm_invoice_head.rep_id==mso_id)
        qset_rsm=qset_rsm(db.sm_invoice_head.rep_id==mso_id)
        qset_total=qset_total(db.sm_invoice_head.rep_id==mso_id)
        
    if (market_id!=''):
        qset=qset(db.sm_invoice_head.msarket_id==msarket_id)
        qset_fm=qset_fm(db.sm_invoice_head.msarket_id==msarket_id)
        qset_rsm=qset_rsm(db.sm_invoice_head.msarket_id==msarket_id)
        qset_total=qset_total(db.sm_invoice_head.msarket_id==msarket_id)
        
  
    records=qset.select(db.sm_invoice_head.ALL,db.sm_invoice_head.id.count(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),orderby=db.sm_invoice_head.level1_id|db.sm_invoice_head.level2_id|db.sm_invoice_head.level3_id,groupby=db.sm_invoice_head.level1_id|db.sm_invoice_head.level2_id|db.sm_invoice_head.level3_id )
#     return db._lastsql
    records_fm=qset_fm.select(db.sm_invoice_head.ALL,db.sm_invoice_head.id.count(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),orderby=db.sm_invoice_head.level2_id,groupby=db.sm_invoice_head.level2_id )
    records_rsm=qset_rsm.select(db.sm_invoice_head.ALL,db.sm_invoice_head.id.count(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),orderby=db.sm_invoice_head.level1_id,groupby=db.sm_invoice_head.level1_id )
    
    records_total=qset_total.select(db.sm_invoice_head.ALL,db.sm_invoice_head.id.count(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),orderby=db.sm_invoice_head.level1_id,groupby=db.sm_invoice_head.level1_id )
    
    
#     records=qset.select(db.sm_invoice.ALL,(db.sm_invoice_head.quantity * db.sm_invoice_head.price).sum(),(db.sm_invoice_head.return_rate *db.sm_invoice_head.return_qty).sum(),db.sm_invoice_head.bonus_qty.sum(),db.sm_invoice_head.return_qty.sum(),db.sm_invoice_head.return_bonus_qty.sum(),orderby=db.sm_invoice.item_name,groupby=db.sm_invoice.area_id ,limitby=limitby)
#     return records_fm
    
#     records_fm=qset_fm.select(db.sm_invoice.ALL,(db.sm_invoice_head.quantity * db.sm_invoice_head.price).sum(),(db.sm_invoice.return_rate *db.sm_invoice_head.return_qty).sum(),db.sm_invoice_head.bonus_qty.sum(),db.sm_invoice_head.return_qty.sum(),db.sm_invoice_head.return_bonus_qty.sum(),orderby=db.sm_invoice_head.item_id,groupby=db.sm_invoice_head.level2_id ,limitby=limitby)
#     records_rsm=qset_rsm.select(db.sm_invoice.ALL,(db.sm_invoice_head.quantity * db.sm_invoice_head.price).sum(),(db.sm_invoice_head.return_rate *db.sm_invoice_head.return_qty).sum(),db.sm_invoice_head.bonus_qty.sum(),db.sm_invoice_head.return_qty.sum(),db.sm_invoice_head.return_bonus_qty.sum(),orderby=db.sm_invoice_head.item_id,groupby=db.sm_invoice_head.level1_id ,limitby=limitby)
#     
#     records_total=qset_total.select(db.sm_invoice.ALL,(db.sm_invoice_head.quantity * db.sm_invoice_head.price).sum(),(db.sm_invoice_head.return_rate *db.sm_invoice_head.return_qty).sum(),db.sm_invoice_head.bonus_qty.sum(),db.sm_invoice_head.return_qty.sum(),db.sm_invoice_head.return_bonus_qty.sum(),orderby=db.sm_invoice.item_name,groupby=db.sm_invoice.level1_id ,limitby=limitby)
#     
#     return records_rsm
            
    if records:  
       
        
        return dict(records=records,records_fm=records_fm,records_rsm=records_rsm,records_total=records_total,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name, teritory_id=teritory_id, teritory_name=teritory_name, mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))


# ===========D===========
def msowiseSDLoad():
    c_id=session.cid
    
    response.title='MSO wise Sales'
    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 

    
    levelRows = db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == teritory_id)).select(db.sm_level.level1,db.sm_level.level2,limitby=(0,1))
#     return levelRows
    if levelRows:
        rsm=levelRows[0].level1
        fm=levelRows[0].level2
#     return fm
    
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)

    qset=qset(db.sm_invoice_head.status=='Invoiced')    
    qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    qset_rsm=db()
    qset_rsm=qset_rsm(db.sm_invoice_head.cid==c_id)
    qset_rsm=qset_rsm(db.sm_invoice_head.status=='Invoiced')  
    qset_rsm=qset_rsm((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    qset_fm=db()
    qset_fm=qset_fm(db.sm_invoice_head.cid==c_id)
#     qset=qset(db.sm_client.cid==c_id)
#     qset=qset(db.sm_client.client_id==db.sm_invoice.client_id)
    qset_fm=qset_fm(db.sm_invoice_head.status=='Invoiced')  
    qset_fm=qset_fm((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    
    qset_total=db()
    qset_total=qset_total(db.sm_invoice_head.cid==c_id)

    qset_total=qset_total(db.sm_invoice_head.status=='Invoiced')  
    qset_total=qset_total((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    if (depot_id!=''):
        qset=qset(db.sm_invoice_head.depot_id==depot_id)
        qset_fm=qset_fm(db.sm_invoice_head.depot_id==depot_id)
        qset_rsm=qset_rsm(db.sm_invoice_head.depot_id==depot_id)
        qset_total=qset_total(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice_head.store_id==store_id)
        qset_fm=qset_fm(db.sm_invoice_head.store_id==store_id)
        qset_rsm=qset_rsm(db.sm_invoice_head.store_id==store_id)
        qset_total=qset_total(db.sm_invoice_head.store_id==store_id)
        
    if (customer_id!=''):
        qset=qset(db.sm_invoice_head.client_id==customer_id)
        qset_fm=qset_fm(db.sm_invoice_head.client_id==customer_id)
        qset_rsm=qset_rsm(db.sm_invoice_head.client_id==customer_id)
        qset_total=qset_total(db.sm_invoice_head.client_id==customer_id)
    
    if (teritory_id!=''):
        qset=qset(db.sm_invoice_head.area_id==teritory_id)
        
        qset_rsm=qset_rsm(db.sm_invoice_head.level1_id==rsm)
        qset_fm=qset_fm(db.sm_invoice_head.level2_id==fm)
        qset_total=qset_total(db.sm_invoice_head.area_id==teritory_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_invoice_head.rep_id==mso_id)
        qset_fm=qset_fm(db.sm_invoice_head.rep_id==mso_id)
        qset_rsm=qset_rsm(db.sm_invoice_head.rep_id==mso_id)
        qset_total=qset_total(db.sm_invoice_head.rep_id==mso_id)
        
    if (market_id!=''):
        qset=qset(db.sm_invoice_head.msarket_id==msarket_id)
        qset_fm=qset_fm(db.sm_invoice_head.msarket_id==msarket_id)
        qset_rsm=qset_rsm(db.sm_invoice_head.msarket_id==msarket_id)
        qset_total=qset_total(db.sm_invoice_head.msarket_id==msarket_id)
        
  
    records=qset.select(db.sm_invoice_head.ALL,db.sm_invoice_head.id.count(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),orderby=db.sm_invoice_head.level1_id|db.sm_invoice_head.level2_id|db.sm_invoice_head.level3_id,groupby=db.sm_invoice_head.level1_id|db.sm_invoice_head.level2_id|db.sm_invoice_head.level3_id )
#     return db._lastsql
    records_fm=qset_fm.select(db.sm_invoice_head.ALL,db.sm_invoice_head.id.count(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),orderby=db.sm_invoice_head.level2_id,groupby=db.sm_invoice_head.level2_id )
    records_rsm=qset_rsm.select(db.sm_invoice_head.ALL,db.sm_invoice_head.id.count(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),orderby=db.sm_invoice_head.level1_id,groupby=db.sm_invoice_head.level1_id )
    
    records_total=qset_total.select(db.sm_invoice_head.ALL,db.sm_invoice_head.id.count(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),orderby=db.sm_invoice_head.level1_id,groupby=db.sm_invoice_head.level1_id )
    
    

    if records:  
       
        myString='MSO wise Sales\n'
        myString=myString+'Date Range,'+date_from+','+date_to+'\n'
        myString=myString+'Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString=myString+'Store,'+store_id+'|'+store_name+'\n'
        myString=myString+'Customer,'+customer_id+'|'+customer_name+'\n'
        myString=myString+'Teritory,'+teritory_id+'|'+teritory_name+'\n\n'
        myString=myString+'MSO,'+mso_id+'|'+mso_name+'\n\n'
        
#         myString=myString+'Total,'+str(customer_count)+'\n\n\n'
        
        myString+='MSO TR ,   MSO Name  ,  Market  ,  Invoice Total  ,  No of Invoive ,   Return Total  ,  Exec %  ,  Returm %  ,  Net Sold \n'
         
        for record in records:
            area_id=record[db.sm_invoice_head.area_id]
            area_name=record[db.sm_invoice_head.area_name]
            market_id=record[db.sm_invoice_head.market_id]
            total_amount=record[db.sm_invoice_head.total_amount.sum()]
            invCount=record[db.sm_invoice_head.id.count()]
            return_amount=record[db.sm_invoice_head.return_tp.sum()] + record[db.sm_invoice_head.return_vat.sum()]-record[db.sm_invoice_head.return_discount.sum()]
            netSold=record[db.sm_invoice_head.total_amount.sum()]-return_amount
            sale=record[db.sm_invoice_head.total_amount.sum()]+record[db.sm_invoice_head.return_discount.sum()]-record[db.sm_invoice_head.return_vat.sum()]
            rSale=return_amount
            eP=(netSold*100)/sale
            rP=(return_amount*100)/sale
            
            
            myString+=str(area_id)+','+str(area_name)+','+str(market_id)+','+str(total_amount)+','+str(invCount)+','+str(return_amount)+','+str(round(eP,2))+','+str(rP)+','+str(netSold)+'\n'
        
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=MSOwiseSales.csv'   
        return str(myString) 
    
    
    
    
    
    
    
    
    
    
    
    
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))

        


#      btn_MSOwiseS   

def catMSOwiseS():
    c_id=session.cid
    
    response.title='Catagory and MSO wise Sales'
    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    customerCat_id=str(request.vars.customerCat_id).strip()
    customerCat_name=str(request.vars.customerCat_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    if customerCat_id=='':        
        session.flash="Please select Teritory and Customer Category"
        redirect(URL(c='report_sales',f='home'))
    
    levelRows = db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == teritory_id)).select(db.sm_level.level1,db.sm_level.level2,limitby=(0,1))
#     return levelRows
    if levelRows:
        rsm=levelRows[0].level1
        fm=levelRows[0].level2
    
    qset=db()
    qset=qset(db.sm_invoice.cid==c_id)
    qset=qset(db.sm_client.cid==c_id)
    qset=qset(db.sm_client.client_id==db.sm_invoice.client_id)
    qset=qset(db.sm_invoice.status=='Invoiced')    
    qset=qset((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
    
    qset_rsm=db()
    qset_rsm=qset_rsm(db.sm_invoice.cid==c_id)
    qset_rsm=qset_rsm(db.sm_client.cid==c_id)
    qset_rsm=qset_rsm(db.sm_client.client_id==db.sm_invoice.client_id)
    qset_rsm=qset_rsm(db.sm_invoice.status=='Invoiced')  
    qset_rsm=qset_rsm((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
    
    qset_fm=db()
    qset_fm=qset_fm(db.sm_invoice.cid==c_id)
    qset_fm=qset_fm(db.sm_client.cid==c_id)
    qset_fm=qset_fm(db.sm_client.client_id==db.sm_invoice.client_id)
    qset_fm=qset_fm(db.sm_invoice.status=='Invoiced')  
    qset_fm=qset_fm((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
    
    
    qset_total=db()
    qset_total=qset_total(db.sm_invoice.cid==c_id)
    qset_total=qset_total(db.sm_client.cid==c_id)
    qset_total=qset_total(db.sm_client.client_id==db.sm_invoice.client_id)
    qset_total=qset_total(db.sm_invoice.status=='Invoiced')  
    qset_total=qset_total((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
    
    if (depot_id!=''):
        qset=qset(db.sm_invoice.depot_id==depot_id)
        qset_fm=qset_fm(db.sm_invoice.depot_id==depot_id)
        qset_rsm=qset_rsm(db.sm_invoice.depot_id==depot_id)
        qset_total=qset_total(db.sm_invoice.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice.store_id==store_id)
        qset_fm=qset_fm(db.sm_invoice.store_id==store_id)
        qset_rsm=qset_rsm(db.sm_invoice.store_id==store_id)
        qset_total=qset_total(db.sm_invoice.store_id==store_id)
        
    if (customer_id!=''):
        qset=qset(db.sm_invoice.client_id==customer_id)
        qset_fm=qset_fm(db.sm_invoice.client_id==customer_id)
        qset_rsm=qset_rsm(db.sm_invoice.client_id==customer_id)
        qset_total=qset_total(db.sm_invoice.client_id==customer_id)
    
    if (customerCat_id!=''):
        qset=qset(db.sm_client.category_id==customerCat_id)
        qset_fm=qset_fm(db.sm_client.category_id==customerCat_id)
        qset_rsm=qset_rsm(db.sm_client.category_id==customerCat_id)
        qset_total=qset_total(db.sm_client.category_id==customerCat_id)
    
    if (teritory_id!=''):
        qset=qset(db.sm_invoice.area_id==teritory_id)
        qset_rsm=qset_rsm(db.sm_invoice.level1_id==rsm)
        qset_fm=qset_fm(db.sm_invoice.level2_id==fm)
        qset_total=qset_total(db.sm_invoice.area_id==teritory_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_invoice.rep_id==mso_id)
        qset_fm=qset_fm(db.sm_invoice.rep_id==mso_id)
        qset_rsm=qset_rsm(db.sm_invoice.rep_id==mso_id)
        qset_total=qset_total(db.sm_invoice.rep_id==mso_id)
        
  
    records=qset.select(db.sm_invoice.ALL,db.sm_client.category_id,db.sm_client.category_name,db.sm_client.market_id, (db.sm_invoice.quantity * db.sm_invoice.price).sum(),(db.sm_invoice.return_rate *db.sm_invoice.return_qty).sum(),db.sm_invoice.bonus_qty.sum(),db.sm_invoice.return_qty.sum(),db.sm_invoice.return_bonus_qty.sum(),orderby=db.sm_invoice.area_id | db.sm_client.category_id,groupby=db.sm_invoice.area_id | db.sm_client.category_id,limitby=limitby)
    records_fm=qset_fm.select(db.sm_invoice.ALL,db.sm_client.category_id,db.sm_client.category_name,db.sm_client.market_id, (db.sm_invoice.quantity * db.sm_invoice.price).sum(),(db.sm_invoice.return_rate *db.sm_invoice.return_qty).sum(),db.sm_invoice.bonus_qty.sum(),db.sm_invoice.return_qty.sum(),db.sm_invoice.return_bonus_qty.sum(),orderby=db.sm_invoice.item_name,groupby=db.sm_invoice.level2_id | db.sm_client.category_id,limitby=limitby)
    records_rsm=qset_rsm.select(db.sm_invoice.ALL,db.sm_client.category_id,db.sm_client.category_name,db.sm_client.market_id, (db.sm_invoice.quantity * db.sm_invoice.price).sum(),(db.sm_invoice.return_rate *db.sm_invoice.return_qty).sum(),db.sm_invoice.bonus_qty.sum(),db.sm_invoice.return_qty.sum(),db.sm_invoice.return_bonus_qty.sum(),orderby=db.sm_invoice.item_name,groupby=db.sm_invoice.level1_id | db.sm_client.category_id,limitby=limitby)
#     return records_rsm
    records_total=qset_total.select(db.sm_invoice.ALL,db.sm_client.category_id,db.sm_client.category_name,db.sm_client.market_id,(db.sm_invoice.quantity * db.sm_invoice.price).sum(),(db.sm_invoice.return_rate *db.sm_invoice.return_qty).sum(),db.sm_invoice.bonus_qty.sum(),db.sm_invoice.return_qty.sum(),db.sm_invoice.return_bonus_qty.sum(),orderby=db.sm_invoice.item_name,limitby=limitby)
    
    reportfmDict={}
    reportfmList=[]
    reportfmmsoList=[]
    
    for records_fm in records_fm:
       mso_tr=records_fm[db.sm_invoice.area_id]
       fm=records_fm[db.sm_invoice.level2_id]
       fm_invTotal=records_fm[(db.sm_invoice.quantity * db.sm_invoice.price).sum()]
       fm_retTotal=records_fm[(db.sm_invoice.return_rate *db.sm_invoice.return_qty).sum()]
       fm_noRet=records_fm[db.sm_invoice.return_qty.sum()]   
       reportfmDict={'mso_tr':mso_tr,'fm':fm,'fm_invTotal':fm_invTotal,'fm_retTotal':fm_retTotal,'fm_noRet':fm_noRet}  
       reportfmList.append(reportfmDict)
       reportfmmsoList.append(mso_tr)
       
    reportrsmDict={}
    reportrsmList=[]
    reportrsmmsoList=[]
#     return records_rsm
    for records_rsm in records_rsm:
       mso_tr_rsm=records_rsm[db.sm_invoice.area_id]
       rsm=records_rsm[db.sm_invoice.level1_id]
       rsm_invTotal=records_rsm[(db.sm_invoice.quantity * db.sm_invoice.price).sum()]
       rsm_retTotal=records_rsm[(db.sm_invoice.return_rate *db.sm_invoice.return_qty).sum()]
       rsm_noRet=records_rsm[db.sm_invoice.return_qty.sum()]   
       reportrsmDict={'mso_tr_rsm':mso_tr_rsm,'rsm':rsm,'rsm_invTotal':rsm_invTotal,'rsm_retTotal':rsm_retTotal,'rsm_noRet':rsm_noRet}  
       reportrsmList.append(reportrsmDict)
       reportrsmmsoList.append(mso_tr_rsm)
    
    if records:  
        return dict(records=records,records_fm=records_fm,records_rsm=records_rsm,records_total=records_total,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name, teritory_id=teritory_id, teritory_name=teritory_name, mso_id=mso_id, mso_name=mso_name,page=page,items_per_page=items_per_page)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
        
        
        
def catDPwiseS():
    c_id=session.cid
    
    response.title='Catagory and MSO wise Sales'
    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    customerCat_id=str(request.vars.customerCat_id).strip()
    customerCat_name=str(request.vars.customerCat_name).strip()
    
    customerCat_id=str(request.vars.customerCat_id).strip()
    customerCat_name=str(request.vars.customerCat_name).strip()
    
    dman_id=str(request.vars.dman_id).strip()
    dman_name=str(request.vars.dman_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging

    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"

    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
    if (dman_id!=''):
        condition=condition+"AND d_man_id = '"+str(dman_id)+"'"        
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"      
    if (customerCat_id!=''):
        condition=condition+"AND category_id = '"+str(customerCat_id)+"'"    
    if (teritory_id!=''):
        condition=condition+"AND area_id = '"+str(teritory_id)+"'"     
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"

    dateRecords="SELECT d_man_id, d_man_name,market_id,category_id, SUM(quantity * actual_tp) as invTP,SUM(actual_tp *return_qty) as retTP,SUM(return_qty) as retQty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY d_man_id, category_id ORDER BY d_man_id, category_id;"
#     return dateRecords
    records=db.executesql(dateRecords,as_dict = True) 


    if records:  
        return dict(records=records,customerCat_id=customerCat_id,customerCat_name=customerCat_name,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name, teritory_id=teritory_id, teritory_name=teritory_name, mso_id=mso_id, mso_name=mso_name,page=page,items_per_page=items_per_page)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
        
def catDPwiseSD():
    c_id=session.cid
    
    response.title='Catagory and MSO wise Sales'
    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    customerCat_id=str(request.vars.customerCat_id).strip()
    customerCat_name=str(request.vars.customerCat_name).strip()
    
    customerCat_id=str(request.vars.customerCat_id).strip()
    customerCat_name=str(request.vars.customerCat_name).strip()
    
    dman_id=str(request.vars.dman_id).strip()
    dman_name=str(request.vars.dman_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging

    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"

    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
    if (dman_id!=''):
        condition=condition+"AND d_man_id = '"+str(dman_id)+"'"        
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"      
    if (customerCat_id!=''):
        condition=condition+"AND category_id = '"+str(customerCat_id)+"'"    
    if (teritory_id!=''):
        condition=condition+"AND area_id = '"+str(teritory_id)+"'"     
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"

    dateRecords="SELECT d_man_id, d_man_name,market_id,category_id, SUM(quantity * actual_tp) as invTP,SUM(actual_tp *return_qty) as retTP,SUM(return_qty) as retQty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY d_man_id, category_id ORDER BY d_man_id, category_id;"
#     return dateRecords
    records=db.executesql(dateRecords,as_dict = True)    
   
    if records:  
        myString='DateRange,'+date_from+','+date_to+'\n'
        myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString+='Store,'+store_id+'|'+store_name+'\n'
        myString+='Area,'+teritory_id+'|'+teritory_name+'\n'
        myString+='Customer,'+customer_id+'|'+customer_name+'\n'
        myString+='MSO,'+mso_id+'|'+mso_name+'\n'
#         myString+='Category,'+customerCat_id+'|'+customerCat_name+'\n\n'
                                        
        myString =myString+ 'DP ID  ,  DP Name  ,Category,Market,   Invoice Total  ,  Return Total  ,  No of Reurn ,   Exec %  ,  Returm %  ,  Net Sold \n' 
                         
        for i in range(len(records)):
            record=records[i]
            netSold=record['invTP']-record['retTP']
            sale=record['invTP']
            rSale=record['retTP']
#             netSoldTotal=netSoldTotal+netSold
#             saleTotal=saleTotal+sale
#             rSaleTotal=rSaleTotal+rSale
            eP=0
            rP=0
            if sale > 0: 
                eP=(netSold*100)/sale 
            if sale > 0: 
                rP=(rSale*100)/sale
            
            
            myString=myString+str(record['d_man_id'])+','+str(record['d_man_name'])+','+str(record['category_id'])+','+str(record['market_id'])+','+str(record['invTP'])+','+str(record['retTP'])+','+str(record['retQty'])+','+str(eP)+','+str(rP)+','+str(netSold)+'\n'
            
    
        #Save as csv
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=ProductWiseSalesStatement.csv'   
        return str(myString)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
# =======================


        
def dpwiseSD():
    c_id=session.cid   
#     return c_id
    response.title='Delivery Person Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    dman_id=str(request.vars.dman_id).strip()
    dman_name=str(request.vars.dman_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  
#     return dman_id
        
#     if (dman_id==""):
#         session.flash="Please select deliery person."
#         redirect(URL(c='report_sales',f='home'))
        
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    qset_fr=db()
    qset_fr=qset_fr(db.sm_invoice_head.cid==c_id)
    qset_fr=qset_fr(db.sm_invoice_head.status=='Invoiced')
    qset_fr=qset_fr((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    qset_fr=qset_fr((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_sp_discount)>0)

    if (depot_id!=''):
        qset=qset(db.sm_invoice_head.depot_id==depot_id)
        qset_fr=qset_fr(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice_head.store_id==store_id)   
        qset_fr=qset_fr(db.sm_invoice_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_invoice_head.client_id==client_id)
        qset_fr=qset_fr(db.sm_invoice_head.client_id==client_id)
    if (teritory_id!=''):
        qset=qset(db.sm_invoice_head.area_id==teritory_id)
        qset_fr=qset_fr(db.sm_invoice_head.area_id==teritory_id)
    if (mso_id!=''):
        qset=qset(db.sm_invoice_head.rep_id==mso_id) 
        qset_fr=qset_fr(db.sm_invoice_head.rep_id==mso_id) 
    if (dman_id!=''):
        qset=qset(db.sm_invoice_head.d_man_id==dman_id)
        qset_fr=qset_fr(db.sm_invoice_head.d_man_id==dman_id) 
    if (market_id!=''):
        qset=qset(db.sm_invoice_head.market_id==market_id)
        qset_fr=qset_fr(db.sm_invoice_head.market_id==market_id)

        
    records=qset.select(db.sm_invoice_head.d_man_id,db.sm_invoice_head.d_man_name,db.sm_invoice_head.id.count(),db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.vat_total_amount.sum(),(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),(db.sm_invoice_head.return_discount+db.sm_invoice_head.return_sp_discount).sum(), orderby=db.sm_invoice_head.d_man_id,groupby=db.sm_invoice_head.d_man_id)
#     return db._lastsql
    
    records_fr=qset_fr.select(db.sm_invoice_head.d_man_id,db.sm_invoice_head.id.count(), orderby=db.sm_invoice_head.d_man_id,groupby=db.sm_invoice_head.d_man_id)
#     return records_fr
#     return db._lastsql
     
    dmanList=[]
    invCList=[]
    for records_fr in records_fr:
        dman_id = records_fr[db.sm_invoice_head.d_man_id]
        invCount = records_fr[db.sm_invoice_head.id.count()]
        dmanList.append(dman_id)
        invCList.append(invCount)
    if records:
        return dict(records=records,dmanList=dmanList,invCList=invCList,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  teritory_id=teritory_id, teritory_name=teritory_name, dman_id=dman_id,dman_name=dman_name, mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name)

    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
        
def dpwiseSDD():
    c_id=session.cid   
#     return c_id
    response.title='Delivery Person Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    dman_id=str(request.vars.dman_id).strip()
    dman_name=str(request.vars.dman_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  
#     return dman_id
        
#     if (dman_id==""):
#         session.flash="Please select deliery person."
#         redirect(URL(c='report_sales',f='home'))
        
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    qset_fr=db()
    qset_fr=qset_fr(db.sm_invoice_head.cid==c_id)
    qset_fr=qset_fr(db.sm_invoice_head.status=='Invoiced')
    qset_fr=qset_fr((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    qset_fr=qset_fr((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_sp_discount)>0)

    if (depot_id!=''):
        qset=qset(db.sm_invoice_head.depot_id==depot_id)
        qset_fr=qset_fr(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice_head.store_id==store_id)   
        qset_fr=qset_fr(db.sm_invoice_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_invoice_head.client_id==client_id)
        qset_fr=qset_fr(db.sm_invoice_head.client_id==client_id)
    if (teritory_id!=''):
        qset=qset(db.sm_invoice_head.area_id==teritory_id)
        qset_fr=qset_fr(db.sm_invoice_head.area_id==teritory_id)
    if (mso_id!=''):
        qset=qset(db.sm_invoice_head.rep_id==mso_id) 
        qset_fr=qset_fr(db.sm_invoice_head.rep_id==mso_id) 
    if (dman_id!=''):
        qset=qset(db.sm_invoice_head.d_man_id==dman_id)
        qset_fr=qset_fr(db.sm_invoice_head.d_man_id==dman_id) 
    if (market_id!=''):
        qset=qset(db.sm_invoice_head.market_id==market_id)
        qset_fr=qset_fr(db.sm_invoice_head.market_id==market_id)

        
    records=qset.select(db.sm_invoice_head.d_man_id,db.sm_invoice_head.d_man_name,db.sm_invoice_head.id.count(),db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.vat_total_amount.sum(),(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),(db.sm_invoice_head.return_discount+db.sm_invoice_head.return_sp_discount).sum(), orderby=db.sm_invoice_head.d_man_id,groupby=db.sm_invoice_head.d_man_id)
#     return records
    
    records_fr=qset_fr.select(db.sm_invoice_head.d_man_id,db.sm_invoice_head.id.count(), orderby=db.sm_invoice_head.d_man_id,groupby=db.sm_invoice_head.d_man_id)
#     return records_fr
#     return db._lastsql
     
    dmanList=[]
    invCList=[]
    for records_fr in records_fr:
        dman_id = records_fr[db.sm_invoice_head.d_man_id]
        invCount = records_fr[db.sm_invoice_head.id.count()]
        dmanList.append(dman_id)
        invCList.append(invCount)
    
    if records:  
        myString='DateRange,'+date_from+','+date_to+'\n'
        myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString+='Store,'+store_id+'|'+store_name+'\n'
        myString+='Area,'+teritory_id+'|'+teritory_name+'\n'
        myString+='Customer,'+customer_id+'|'+customer_name+'\n'
        myString+='MSO,'+mso_id+'|'+mso_name+'\n'
#         myString+='Category,'+customerCat_id+'|'+customerCat_name+'\n\n'
                                        
        myString =myString+ 'DP ID  ,  DP Name  ,  Inv Count  ,  Invoice Total  ,  Return Total  ,  No of Reurn ,   Exec %  ,  Returm %  ,  Net Sold \n' 
                         
        for records in records:
            retCount=0
            d_man_id=records[db.sm_invoice_head.d_man_id]
#             return d_man_id
            if [s for s in dmanList if d_man_id in s]:
                
               index_element = dmanList.index(d_man_id)           
               retCount=invCList[index_element]
                
            retAmn=records[(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_sp_discount).sum()]
            invAmn=(records[db.sm_invoice_head.actual_total_tp.sum()])     
            netSold=0
            sale=records[db.sm_invoice_head.actual_total_tp.sum()]
            netSold=records[db.sm_invoice_head.actual_total_tp.sum()]-retAmn
            
            
            
            
            
            eP=(netSold*100)/sale
            rP=(retAmn*100)/sale
            
            myString=myString+str(records[db.sm_invoice_head.d_man_id])+','+str(records[db.sm_invoice_head.d_man_name])+','+str(records[db.sm_invoice_head.id.count()])+','+str(retCount)+','+str(records[db.sm_invoice_head.actual_total_tp.sum()])+','+str(records[(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_sp_discount).sum()])+','+str(eP)+','+str(rP)+','+str(invAmn-retAmn)+'\n'
            
#         for records_total in records_total:
#             netSold=records_total[(db.sm_invoice.quantity * db.sm_invoice.price).sum()]-record[(db.sm_invoice.return_rate *db.sm_invoice.return_qty).sum()]
#             sale=records_total[(db.sm_invoice.quantity * db.sm_invoice.price).sum()]
#             rSale=records_total[(db.sm_invoice.return_rate * db.sm_invoice.return_qty).sum()]
#             eP=(netSold*100)/sale
#             rP=(rSale*100)/sale
#             myString=myString+'\n\n\nTotal for City: '+',,,'+str(round(records_total[(db.sm_invoice.quantity * db.sm_invoice.price).sum()],2))+','+str(round(records_total[(db.sm_invoice.return_rate *db.sm_invoice.return_qty).sum()],2))+','+str(records_total[db.sm_invoice.return_qty.sum()])+','+str(round(eP,2)) +','+str(round(rP,2))+','+str(round(netSold,2))      
    
        #Save as csv
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=ProductWiseSalesStatement.csv'   
        return str(myString)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
# =================================================        
#         customrProductwiseS
def customrProductwiseS():
    
    c_id=session.cid   
    response.title='Customer-Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()

    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    if (teritory_id==''):
        session.flash="Please select a Teritory"
        redirect(URL(c='report_sales',f='home'))
        
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    levelRows = db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == teritory_id)).select(db.sm_level.level1,db.sm_level.level2,limitby=(0,1))
    if levelRows:
        rsm=levelRows[0].level1
        fm=levelRows[0].level2
 
    
    
    condition=''
    conditionRsm=''
    conditionFm=''
    conditionTr=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
        
        conditionRsm=conditionRsm+"AND depot_id = '"+str(depot_id)+"'"
        conditionFm=conditionFm+"AND depot_id = '"+str(depot_id)+"'"
        conditionTr=conditionTr+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        
        conditionRsm=conditionRsm+"AND store_id = '"+str(store_id)+"'"
        conditionFm=conditionFm+"AND store_id = '"+str(store_id)+"'"
        conditionTr=conditionTr+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
        
        conditionRsm=conditionRsm+"AND client_id = '"+str(customer_id)+"'"
        conditionFm=conditionFm+"AND client_id = '"+str(customer_id)+"'"
        conditionTr=conditionTr+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        
        conditionRsm=conditionRsm+"AND rep_id = '"+str(mso_id)+"'"
        conditionFm=conditionFm+"AND rep_id = '"+str(mso_id)+"'"
        conditionTr=conditionTr+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
        
        conditionRsm=conditionRsm+"AND market_id = '"+str(market_id)+"'"
        conditionFm=conditionFm+"AND market_id = '"+str(market_id)+"'"
        conditionTr=conditionTr+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
        
        conditionRsm=conditionRsm+"AND area_id = '"+str(teritory_id)+"'"
        conditionFm=conditionFm+"AND area_id = '"+str(teritory_id)+"'"
        conditionTr=conditionTr+"AND area_id = '"+str(teritory_id)+"'"
    
    
    records_S="SELECT  client_id,client_name,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY client_id,item_id ORDER BY client_id,item_id;"
    records=db.executesql(records_S,as_dict = True) 
    

    records_rsmS="SELECT  level1_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionRsm+"  GROUP BY level1_id ORDER BY level1_id;"
    records_fpS="SELECT  level2_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionFm+"  GROUP BY level2_id ORDER BY level2_id;"
    records_trS="SELECT  level3_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionTr+"  GROUP BY level3_id ORDER BY level3_id;"

    records_rsm=db.executesql(records_rsmS,as_dict = True)
    records_fp=db.executesql(records_fpS,as_dict = True)
    records_tr=db.executesql(records_trS,as_dict = True)
    
    
    if records:
        return dict(records=records,records_rsm=records_rsm,records_tr=records_tr,records_fp=records_fp,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  teritory_id=teritory_id, teritory_name=teritory_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,page=page,items_per_page=items_per_page)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
        
def customrProductwiseSD():
    c_id=session.cid   
    response.title='Customer-Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()

    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    if (teritory_id==''):
        session.flash="Please select a Teritory"
        redirect(URL(c='report_sales',f='home'))
        
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    levelRows = db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == teritory_id)).select(db.sm_level.level1,db.sm_level.level2,limitby=(0,1))
    if levelRows:
        rsm=levelRows[0].level1
        fm=levelRows[0].level2
 
    
    
    condition=''
    conditionRsm=''
    conditionFm=''
    conditionTr=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
        
        conditionRsm=conditionRsm+"AND depot_id = '"+str(depot_id)+"'"
        conditionFm=conditionFm+"AND depot_id = '"+str(depot_id)+"'"
        conditionTr=conditionTr+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        
        conditionRsm=conditionRsm+"AND store_id = '"+str(store_id)+"'"
        conditionFm=conditionFm+"AND store_id = '"+str(store_id)+"'"
        conditionTr=conditionTr+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
        
        conditionRsm=conditionRsm+"AND client_id = '"+str(customer_id)+"'"
        conditionFm=conditionFm+"AND client_id = '"+str(customer_id)+"'"
        conditionTr=conditionTr+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        
        conditionRsm=conditionRsm+"AND rep_id = '"+str(mso_id)+"'"
        conditionFm=conditionFm+"AND rep_id = '"+str(mso_id)+"'"
        conditionTr=conditionTr+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
        
        conditionRsm=conditionRsm+"AND market_id = '"+str(market_id)+"'"
        conditionFm=conditionFm+"AND market_id = '"+str(market_id)+"'"
        conditionTr=conditionTr+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
        
        conditionRsm=conditionRsm+"AND area_id = '"+str(teritory_id)+"'"
        conditionFm=conditionFm+"AND area_id = '"+str(teritory_id)+"'"
        conditionTr=conditionTr+"AND area_id = '"+str(teritory_id)+"'"
    
    
    records_S="SELECT  client_id,client_name,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY client_id,item_id ORDER BY client_id,item_id;"
    records=db.executesql(records_S,as_dict = True) 
    

    records_rsmS="SELECT  level1_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionRsm+"  GROUP BY level1_id ORDER BY level1_id;"
    records_fpS="SELECT  level2_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionFm+"  GROUP BY level2_id ORDER BY level2_id;"
    records_trS="SELECT  level3_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionTr+"  GROUP BY level3_id ORDER BY level3_id;"

    records_rsm=db.executesql(records_rsmS,as_dict = True)
    records_fp=db.executesql(records_fpS,as_dict = True)
    records_tr=db.executesql(records_trS,as_dict = True)
    if records:
        myString='DateRange,'+date_from+','+date_to+'\n'
        myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString+='Store,'+store_id+'|'+store_name+'\n'
        myString+='Area,'+teritory_id+'|'+teritory_name+'\n'
        myString+='Customer,'+customer_id+'|'+customer_name+'\n'
        myString+='MSO,'+mso_id+'|'+mso_name+'\n'
        myString+='Market,'+market_id+'|'+market_name+'\n\n'
                                        
        myString =myString+ '  ,  Ret%   , InvioceQnty   , InvioceBonus  ,  InvioceTradePrice ,ReturnQnty   , ReturnBonus  ,  ReturnTradePrice ,NetQnty  ,  NetBonus  ,  NetTradePrice\n' 
        for i in range(len(records_rsm)):
            record_rsm=records_rsm[i]
            netSoldRsm=record_rsm['actual_tp']-record_rsm['retTP']
            saleRsm=record_rsm['actual_tp']
            rSaleRsm=record_rsm['retTP']
            rP_rsm=0
            if (rSaleRsm > 0):
                rP_rsm=(rSale_rsm*100)/sale_rsm
            myString =myString+ 'RSM,'+str(record_rsm['level1_id'])+','+str(rP_rsm)+','+str(record_rsm['inv_qty'])+','+str(record_rsm['inv_bonus_qty'])+','+str(record_rsm['actual_tp'])+','+str(record_rsm['ret_qty'])+','+str(record_rsm['ret_bonus_qty'])+','+str(record_rsm['retTP'])+','+str(record_rsm['inv_qty']-record_rsm['ret_qty'])+','+str(record_rsm['inv_bonus_qty']-record_rsm['ret_bonus_qty'])+','+str(netSoldRsm)+'\n'
        
        for i in range(len(records_fp)):
            record_fp=records_fp[i]
            netSold_fp=record_fp['actual_tp']-record_fp['retTP']
            sale_fp=record_fp['actual_tp']
            rSale_fp=record_fp['retTP']
            rP_fp=0
            if (rSale_fp > 0):
                rP_fp=(rSale_fp*100)/sale_fp
            myString =myString+ 'FM,'+str(record_fp['level2_id'])+','+str(rP_fp)+','+str(record_fp['inv_qty'])+','+str(record_fp['inv_bonus_qty'])+','+str(record_fp['actual_tp'])+','+str(record_fp['ret_qty'])+','+str(record_fp['ret_bonus_qty'])+','+str(record_fp['retTP'])+','+str(record_fp['inv_qty']-record_fp['ret_qty'])+','+str(record_fp['inv_bonus_qty']-record_fp['ret_bonus_qty'])+','+str(netSold_fp)+'\n'

        for i in range(len(records_tr)):
            record_tr=records_tr[i]
            netSold_tr=record_tr['actual_tp']-record_tr['retTP']
            sale_tr=record_tr['actual_tp']
            rSale_tr=record_tr['retTP']
            rP_tr=0
            if (rSale_tr > 0):
                rP_tr=(rSale_tr*100)/sale_tr
            myString =myString+ 'TR,'+str(record_tr['level3_id'])+','+str(rP_tr)+','+str(record_tr['inv_qty'])+','+str(record_tr['inv_bonus_qty'])+','+str(record_tr['actual_tp'])+','+str(record_tr['ret_qty'])+','+str(record_tr['ret_bonus_qty'])+','+str(record_tr['retTP'])+','+str(record_tr['inv_qty']-record_tr['ret_qty'])+','+str(record_tr['inv_bonus_qty']-record_tr['ret_bonus_qty'])+','+str(netSold_tr)+'\n'
       
       
        myString =myString+ '\n\nClientID,ClientName,ItemID ,   ItemName  ,  UOM  ,  UnitPrice ,   Ret% , InvioceQnty  ,  InvioceBonus  ,  InvioceTradePrice ,ReturnQnty   , ReturnBonus  ,  ReturnTradePrice ,NetQnty  ,  NetBonus ,   NetTradePrice \n'
        p=0
        clientID=''
        for i in range(len(records)):
            record=records[i]
            myString =myString+str(record['client_id'])+',' +str(record['client_name'])+','
                    
            netSold=record['actual_tp']-record['retTP']
            sale=record['actual_tp']
            rSale=record['retTP']
            rP=0
            if (rSale > 0):
                rP=(rSale*100)/sale
            myString=myString+str(record['item_id']+','+str(record['item_name'])+','+str(record['item_unit'])+','+str(round(record['actual_tp']))+','+str(rP)+','+str(record['inv_qty'])+','+str(record['inv_bonus_qty'])+','+str(record['actual_tp'])+','+str(record['ret_qty'])+','+str(record['ret_bonus_qty'])+','+str(record['retTP'])+','+str(record['inv_qty']-record['ret_qty'])+','+str(record['inv_bonus_qty']-record['ret_bonus_qty'])+','+str(netSold))+'\n'
            clientID=record['client_id']
        
        #Save as csv
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=CustomerProductWiseSalesStatement.csv'   
        return str(myString)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))        
# =============================================       
def customrProductwiseSIncludingBonus():
    c_id=session.cid   
    response.title='Customer-Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()

    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    if (teritory_id==''):
        session.flash="Please select a Teritory"
        redirect(URL(c='report_sales',f='home'))
        
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    levelRows = db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == teritory_id)).select(db.sm_level.level1,db.sm_level.level2,limitby=(0,1))
    if levelRows:
        rsm=levelRows[0].level1
        fm=levelRows[0].level2
        
    condition=''
    conditionRsm=''
    conditionFm=''
    conditionTr=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
        
        conditionRsm=conditionRsm+"AND depot_id = '"+str(depot_id)+"'"
        conditionFm=conditionFm+"AND depot_id = '"+str(depot_id)+"'"
        conditionTr=conditionTr+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        
        conditionRsm=conditionRsm+"AND store_id = '"+str(store_id)+"'"
        conditionFm=conditionFm+"AND store_id = '"+str(store_id)+"'"
        conditionTr=conditionTr+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
        
        conditionRsm=conditionRsm+"AND client_id = '"+str(customer_id)+"'"
        conditionFm=conditionFm+"AND client_id = '"+str(customer_id)+"'"
        conditionTr=conditionTr+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        
        conditionRsm=conditionRsm+"AND rep_id = '"+str(mso_id)+"'"
        conditionFm=conditionFm+"AND rep_id = '"+str(mso_id)+"'"
        conditionTr=conditionTr+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
        
        conditionRsm=conditionRsm+"AND market_id = '"+str(market_id)+"'"
        conditionFm=conditionFm+"AND market_id = '"+str(market_id)+"'"
        conditionTr=conditionTr+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
        
        conditionRsm=conditionRsm+"AND area_id = '"+str(teritory_id)+"'"
        conditionFm=conditionFm+"AND area_id = '"+str(teritory_id)+"'"
        conditionTr=conditionTr+"AND area_id = '"+str(teritory_id)+"'"
    
    
    records_S="SELECT  client_id,client_name,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty > 0 AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY client_id,item_id ORDER BY client_id,item_id;"
    records=db.executesql(records_S,as_dict = True) 
    

    records_rsmS="SELECT  level1_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty > 0 AND    invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionRsm+"  GROUP BY level1_id ORDER BY level1_id;"
    records_fpS="SELECT  level2_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty > 0 AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionFm+"  GROUP BY level2_id ORDER BY level2_id;"
    records_trS="SELECT  level3_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty > 0 AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionTr+"  GROUP BY level3_id ORDER BY level3_id;"

    records_rsm=db.executesql(records_rsmS,as_dict = True)
    records_fp=db.executesql(records_fpS,as_dict = True)
    records_tr=db.executesql(records_trS,as_dict = True)
    
    if records:
        return dict(records=records,records_rsm=records_rsm,records_tr=records_tr,records_fp=records_fp,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  teritory_id=teritory_id, teritory_name=teritory_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,page=page,items_per_page=items_per_page)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
        
def customrProductwiseSIncludingBonusD():
    c_id=session.cid   
    response.title='Customer-Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()

    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    if (teritory_id==''):
        session.flash="Please select a Teritory"
        redirect(URL(c='report_sales',f='home'))
        
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    levelRows = db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == teritory_id)).select(db.sm_level.level1,db.sm_level.level2,limitby=(0,1))
    if levelRows:
        rsm=levelRows[0].level1
        fm=levelRows[0].level2
 
    
    
    condition=''
    conditionRsm=''
    conditionFm=''
    conditionTr=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
        
        conditionRsm=conditionRsm+"AND depot_id = '"+str(depot_id)+"'"
        conditionFm=conditionFm+"AND depot_id = '"+str(depot_id)+"'"
        conditionTr=conditionTr+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        
        conditionRsm=conditionRsm+"AND store_id = '"+str(store_id)+"'"
        conditionFm=conditionFm+"AND store_id = '"+str(store_id)+"'"
        conditionTr=conditionTr+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
        
        conditionRsm=conditionRsm+"AND client_id = '"+str(customer_id)+"'"
        conditionFm=conditionFm+"AND client_id = '"+str(customer_id)+"'"
        conditionTr=conditionTr+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        
        conditionRsm=conditionRsm+"AND rep_id = '"+str(mso_id)+"'"
        conditionFm=conditionFm+"AND rep_id = '"+str(mso_id)+"'"
        conditionTr=conditionTr+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
        
        conditionRsm=conditionRsm+"AND market_id = '"+str(market_id)+"'"
        conditionFm=conditionFm+"AND market_id = '"+str(market_id)+"'"
        conditionTr=conditionTr+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
        
        conditionRsm=conditionRsm+"AND area_id = '"+str(teritory_id)+"'"
        conditionFm=conditionFm+"AND area_id = '"+str(teritory_id)+"'"
        conditionTr=conditionTr+"AND area_id = '"+str(teritory_id)+"'"
    
    
    records_S="SELECT  client_id,client_name,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty > 0 AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY client_id,item_id ORDER BY client_id,item_id;"
    records=db.executesql(records_S,as_dict = True) 
    

    records_rsmS="SELECT  level1_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty > 0 AND invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionRsm+"  GROUP BY level1_id ORDER BY level1_id;"
    records_fpS="SELECT  level2_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced'  AND bonus_qty > 0 AND invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionFm+"  GROUP BY level2_id ORDER BY level2_id;"
    records_trS="SELECT  level3_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced'  AND bonus_qty > 0 AND invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionTr+"  GROUP BY level3_id ORDER BY level3_id;"

    records_rsm=db.executesql(records_rsmS,as_dict = True)
    records_fp=db.executesql(records_fpS,as_dict = True)
    records_tr=db.executesql(records_trS,as_dict = True)
    if records:
        myString='DateRange,'+date_from+','+date_to+'\n'
        myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString+='Store,'+store_id+'|'+store_name+'\n'
        myString+='Area,'+teritory_id+'|'+teritory_name+'\n'
        myString+='Customer,'+customer_id+'|'+customer_name+'\n'
        myString+='MSO,'+mso_id+'|'+mso_name+'\n'
        myString+='Market,'+market_id+'|'+market_name+'\n\n'
                                        
        myString =myString+ '  ,  Ret%   , InvioceQnty   , InvioceBonus  ,  InvioceTradePrice ,ReturnQnty   , ReturnBonus  ,  ReturnTradePrice ,NetQnty  ,  NetBonus  ,  NetTradePrice\n' 
        for i in range(len(records_rsm)):
            record_rsm=records_rsm[i]
            netSoldRsm=record_rsm['actual_tp']-record_rsm['retTP']
            saleRsm=record_rsm['actual_tp']
            rSaleRsm=record_rsm['retTP']
            rP_rsm=0
            if (rSaleRsm > 0):
                rP_rsm=(rSale_rsm*100)/sale_rsm
            myString =myString+ 'RSM,'+str(record_rsm['level1_id'])+','+str(rP_rsm)+','+str(record_rsm['inv_qty'])+','+str(record_rsm['inv_bonus_qty'])+','+str(record_rsm['actual_tp'])+','+str(record_rsm['ret_qty'])+','+str(record_rsm['ret_bonus_qty'])+','+str(record_rsm['retTP'])+','+str(record_rsm['inv_qty']-record_rsm['ret_qty'])+','+str(record_rsm['inv_bonus_qty']-record_rsm['ret_bonus_qty'])+','+str(netSoldRsm)+'\n'
        
        for i in range(len(records_fp)):
            record_fp=records_fp[i]
            netSold_fp=record_fp['actual_tp']-record_fp['retTP']
            sale_fp=record_fp['actual_tp']
            rSale_fp=record_fp['retTP']
            rP_fp=0
            if (rSale_fp > 0):
                rP_fp=(rSale_fp*100)/sale_fp
            myString =myString+ 'FM,'+str(record_fp['level2_id'])+','+str(rP_fp)+','+str(record_fp['inv_qty'])+','+str(record_fp['inv_bonus_qty'])+','+str(record_fp['actual_tp'])+','+str(record_fp['ret_qty'])+','+str(record_fp['ret_bonus_qty'])+','+str(record_fp['retTP'])+','+str(record_fp['inv_qty']-record_fp['ret_qty'])+','+str(record_fp['inv_bonus_qty']-record_fp['ret_bonus_qty'])+','+str(netSold_fp)+'\n'

        for i in range(len(records_tr)):
            record_tr=records_tr[i]
            netSold_tr=record_tr['actual_tp']-record_tr['retTP']
            sale_tr=record_tr['actual_tp']
            rSale_tr=record_tr['retTP']
            rP_tr=0
            if (rSale_tr > 0):
                rP_tr=(rSale_tr*100)/sale_tr
            myString =myString+ 'TR,'+str(record_tr['level3_id'])+','+str(rP_tr)+','+str(record_tr['inv_qty'])+','+str(record_tr['inv_bonus_qty'])+','+str(record_tr['actual_tp'])+','+str(record_tr['ret_qty'])+','+str(record_tr['ret_bonus_qty'])+','+str(record_tr['retTP'])+','+str(record_tr['inv_qty']-record_tr['ret_qty'])+','+str(record_tr['inv_bonus_qty']-record_tr['ret_bonus_qty'])+','+str(netSold_tr)+'\n'
       
       
        myString =myString+ '\n\nClientID,ClientName,ItemID ,   ItemName  ,  UOM  ,  UnitPrice ,   Ret% , InvioceQnty  ,  InvioceBonus  ,  InvioceTradePrice ,ReturnQnty   , ReturnBonus  ,  ReturnTradePrice ,NetQnty  ,  NetBonus ,   NetTradePrice \n'
        p=0
        clientID=''
        for i in range(len(records)):
            record=records[i]
            myString =myString+str(record['client_id'])+',' +str(record['client_name'])+','
                    
            netSold=record['actual_tp']-record['retTP']
            sale=record['actual_tp']
            rSale=record['retTP']
            rP=0
            if (rSale > 0):
                rP=(rSale*100)/sale
            myString=myString+str(record['item_id']+','+str(record['item_name'])+','+str(record['item_unit'])+','+str(round(record['actual_tp']))+','+str(rP)+','+str(record['inv_qty'])+','+str(record['inv_bonus_qty'])+','+str(record['actual_tp'])+','+str(record['ret_qty'])+','+str(record['ret_bonus_qty'])+','+str(record['retTP'])+','+str(record['inv_qty']-record['ret_qty'])+','+str(record['inv_bonus_qty']-record['ret_bonus_qty'])+','+str(netSold))+'\n'
            clientID=record['client_id']
        
        #Save as csv
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=CustomerProductWiseSalesStatementWithBonus.csv'   
        return str(myString)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
# =======================================================

        
def customrProductwiseSExcludingBonus():
    c_id=session.cid   
    response.title='Customer-Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    if (teritory_id==''):
        session.flash="Please select a Teritory"
        redirect(URL(c='report_sales',f='home'))
        
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    levelRows = db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == teritory_id)).select(db.sm_level.level1,db.sm_level.level2,limitby=(0,1))
    if levelRows:
        rsm=levelRows[0].level1
        fm=levelRows[0].level2
    
    
    
    condition=''
    conditionRsm=''
    conditionFm=''
    conditionTr=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
        
        conditionRsm=conditionRsm+"AND depot_id = '"+str(depot_id)+"'"
        conditionFm=conditionFm+"AND depot_id = '"+str(depot_id)+"'"
        conditionTr=conditionTr+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        
        conditionRsm=conditionRsm+"AND store_id = '"+str(store_id)+"'"
        conditionFm=conditionFm+"AND store_id = '"+str(store_id)+"'"
        conditionTr=conditionTr+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
        
        conditionRsm=conditionRsm+"AND client_id = '"+str(customer_id)+"'"
        conditionFm=conditionFm+"AND client_id = '"+str(customer_id)+"'"
        conditionTr=conditionTr+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        
        conditionRsm=conditionRsm+"AND rep_id = '"+str(mso_id)+"'"
        conditionFm=conditionFm+"AND rep_id = '"+str(mso_id)+"'"
        conditionTr=conditionTr+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
        
        conditionRsm=conditionRsm+"AND market_id = '"+str(market_id)+"'"
        conditionFm=conditionFm+"AND market_id = '"+str(market_id)+"'"
        conditionTr=conditionTr+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
        
        conditionRsm=conditionRsm+"AND area_id = '"+str(teritory_id)+"'"
        conditionFm=conditionFm+"AND area_id = '"+str(teritory_id)+"'"
        conditionTr=conditionTr+"AND area_id = '"+str(teritory_id)+"'"
    
    
    records_S="SELECT  client_id,client_name,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty = 0 AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY client_id,item_id ORDER BY client_id,item_id;"
    records=db.executesql(records_S,as_dict = True) 
    

    records_rsmS="SELECT  level1_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty = 0 AND    invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionRsm+"  GROUP BY level1_id ORDER BY level1_id;"
    records_fpS="SELECT  level2_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty = 0 AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionFm+"  GROUP BY level2_id ORDER BY level2_id;"
    records_trS="SELECT  level3_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty = 0 AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionTr+"  GROUP BY level3_id ORDER BY level3_id;"

    records_rsm=db.executesql(records_rsmS,as_dict = True)
    records_fp=db.executesql(records_fpS,as_dict = True)
    records_tr=db.executesql(records_trS,as_dict = True)

    if records:
        return dict(records=records,records_rsm=records_rsm,records_tr=records_tr,records_fp=records_fp,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  teritory_id=teritory_id, teritory_name=teritory_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,page=page,items_per_page=items_per_page)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))  

def customrProductwiseSExcludingBonusD():
    c_id=session.cid   
    response.title='Customer-Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()

    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    if (teritory_id==''):
        session.flash="Please select a Teritory"
        redirect(URL(c='report_sales',f='home'))
        
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    levelRows = db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == teritory_id)).select(db.sm_level.level1,db.sm_level.level2,limitby=(0,1))
    if levelRows:
        rsm=levelRows[0].level1
        fm=levelRows[0].level2
 
    
    
    condition=''
    conditionRsm=''
    conditionFm=''
    conditionTr=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
        
        conditionRsm=conditionRsm+"AND depot_id = '"+str(depot_id)+"'"
        conditionFm=conditionFm+"AND depot_id = '"+str(depot_id)+"'"
        conditionTr=conditionTr+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        
        conditionRsm=conditionRsm+"AND store_id = '"+str(store_id)+"'"
        conditionFm=conditionFm+"AND store_id = '"+str(store_id)+"'"
        conditionTr=conditionTr+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
        
        conditionRsm=conditionRsm+"AND client_id = '"+str(customer_id)+"'"
        conditionFm=conditionFm+"AND client_id = '"+str(customer_id)+"'"
        conditionTr=conditionTr+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        
        conditionRsm=conditionRsm+"AND rep_id = '"+str(mso_id)+"'"
        conditionFm=conditionFm+"AND rep_id = '"+str(mso_id)+"'"
        conditionTr=conditionTr+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
        
        conditionRsm=conditionRsm+"AND market_id = '"+str(market_id)+"'"
        conditionFm=conditionFm+"AND market_id = '"+str(market_id)+"'"
        conditionTr=conditionTr+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
        
        conditionRsm=conditionRsm+"AND area_id = '"+str(teritory_id)+"'"
        conditionFm=conditionFm+"AND area_id = '"+str(teritory_id)+"'"
        conditionTr=conditionTr+"AND area_id = '"+str(teritory_id)+"'"
    
    
    records_S="SELECT  client_id,client_name,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty = 0 AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY client_id,item_id ORDER BY client_id,item_id;"
    records=db.executesql(records_S,as_dict = True) 
    

    records_rsmS="SELECT  level1_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty = 0 AND invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionRsm+"  GROUP BY level1_id ORDER BY level1_id;"
    records_fpS="SELECT  level2_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced'  AND bonus_qty = 0 AND invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionFm+"  GROUP BY level2_id ORDER BY level2_id;"
    records_trS="SELECT  level3_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced'  AND bonus_qty = 0 AND invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionTr+"  GROUP BY level3_id ORDER BY level3_id;"

    records_rsm=db.executesql(records_rsmS,as_dict = True)
    records_fp=db.executesql(records_fpS,as_dict = True)
    records_tr=db.executesql(records_trS,as_dict = True)
    if records:
        myString='DateRange,'+date_from+','+date_to+'\n'
        myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString+='Store,'+store_id+'|'+store_name+'\n'
        myString+='Area,'+teritory_id+'|'+teritory_name+'\n'
        myString+='Customer,'+customer_id+'|'+customer_name+'\n'
        myString+='MSO,'+mso_id+'|'+mso_name+'\n'
        myString+='Market,'+market_id+'|'+market_name+'\n\n'
                                        
        myString =myString+ '  ,  Ret%   , InvioceQnty   , InvioceBonus  ,  InvioceTradePrice ,ReturnQnty   , ReturnBonus  ,  ReturnTradePrice ,NetQnty  ,  NetBonus  ,  NetTradePrice\n' 
        for i in range(len(records_rsm)):
            record_rsm=records_rsm[i]
            netSoldRsm=record_rsm['actual_tp']-record_rsm['retTP']
            saleRsm=record_rsm['actual_tp']
            rSaleRsm=record_rsm['retTP']
            rP_rsm=0
            if (rSaleRsm > 0):
                rP_rsm=(rSale_rsm*100)/sale_rsm
            myString =myString+ 'RSM,'+str(record_rsm['level1_id'])+','+str(rP_rsm)+','+str(record_rsm['inv_qty'])+','+str(record_rsm['inv_bonus_qty'])+','+str(record_rsm['actual_tp'])+','+str(record_rsm['ret_qty'])+','+str(record_rsm['ret_bonus_qty'])+','+str(record_rsm['retTP'])+','+str(record_rsm['inv_qty']-record_rsm['ret_qty'])+','+str(record_rsm['inv_bonus_qty']-record_rsm['ret_bonus_qty'])+','+str(netSoldRsm)+'\n'
        
        for i in range(len(records_fp)):
            record_fp=records_fp[i]
            netSold_fp=record_fp['actual_tp']-record_fp['retTP']
            sale_fp=record_fp['actual_tp']
            rSale_fp=record_fp['retTP']
            rP_fp=0
            if (rSale_fp > 0):
                rP_fp=(rSale_fp*100)/sale_fp
            myString =myString+ 'FM,'+str(record_fp['level2_id'])+','+str(rP_fp)+','+str(record_fp['inv_qty'])+','+str(record_fp['inv_bonus_qty'])+','+str(record_fp['actual_tp'])+','+str(record_fp['ret_qty'])+','+str(record_fp['ret_bonus_qty'])+','+str(record_fp['retTP'])+','+str(record_fp['inv_qty']-record_fp['ret_qty'])+','+str(record_fp['inv_bonus_qty']-record_fp['ret_bonus_qty'])+','+str(netSold_fp)+'\n'

        for i in range(len(records_tr)):
            record_tr=records_tr[i]
            netSold_tr=record_tr['actual_tp']-record_tr['retTP']
            sale_tr=record_tr['actual_tp']
            rSale_tr=record_tr['retTP']
            rP_tr=0
            if (rSale_tr > 0):
                rP_tr=(rSale_tr*100)/sale_tr
            myString =myString+ 'TR,'+str(record_tr['level3_id'])+','+str(rP_tr)+','+str(record_tr['inv_qty'])+','+str(record_tr['inv_bonus_qty'])+','+str(record_tr['actual_tp'])+','+str(record_tr['ret_qty'])+','+str(record_tr['ret_bonus_qty'])+','+str(record_tr['retTP'])+','+str(record_tr['inv_qty']-record_tr['ret_qty'])+','+str(record_tr['inv_bonus_qty']-record_tr['ret_bonus_qty'])+','+str(netSold_tr)+'\n'
       
       
        myString =myString+ '\n\nClientID,ClientName,ItemID ,   ItemName  ,  UOM  ,  UnitPrice ,   Ret% , InvioceQnty  ,  InvioceBonus  ,  InvioceTradePrice ,ReturnQnty   , ReturnBonus  ,  ReturnTradePrice ,NetQnty  ,  NetBonus ,   NetTradePrice \n'
        p=0
        clientID=''
        for i in range(len(records)):
            record=records[i]
            myString =myString+str(record['client_id'])+',' +str(record['client_name'])+','
                    
            netSold=record['actual_tp']-record['retTP']
            sale=record['actual_tp']
            rSale=record['retTP']
            rP=0
            if (rSale > 0):
                rP=(rSale*100)/sale
            myString=myString+str(record['item_id']+','+str(record['item_name'])+','+str(record['item_unit'])+','+str(round(record['actual_tp']))+','+str(rP)+','+str(record['inv_qty'])+','+str(record['inv_bonus_qty'])+','+str(record['actual_tp'])+','+str(record['ret_qty'])+','+str(record['ret_bonus_qty'])+','+str(record['retTP'])+','+str(record['inv_qty']-record['ret_qty'])+','+str(record['inv_bonus_qty']-record['ret_bonus_qty'])+','+str(netSold))+'\n'
            clientID=record['client_id']
        
        #Save as csv
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=CustomerProductWiseSalesStatementWithoutBonus.csv'   
        return str(myString)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))  

# ============================================     
#         productwiseS
def productwiseS():
    c_id=session.cid   
    response.title='Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()

    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    if (teritory_id==''):
        session.flash="Please select a Teritory"
        redirect(URL(c='report_sales',f='home'))
        
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    levelRows = db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == teritory_id)).select(db.sm_level.level1,db.sm_level.level2,limitby=(0,1))
    if levelRows:
        rsm=levelRows[0].level1
        fm=levelRows[0].level2
       

#     ===================
    condition=''
    conditionRsm=''
    conditionFm=''
    conditionTr=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
        
        conditionRsm=conditionRsm+"AND depot_id = '"+str(depot_id)+"'"
        conditionFm=conditionFm+"AND depot_id = '"+str(depot_id)+"'"
        conditionTr=conditionTr+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        
        conditionRsm=conditionRsm+"AND store_id = '"+str(store_id)+"'"
        conditionFm=conditionFm+"AND store_id = '"+str(store_id)+"'"
        conditionTr=conditionTr+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
        
        conditionRsm=conditionRsm+"AND client_id = '"+str(customer_id)+"'"
        conditionFm=conditionFm+"AND client_id = '"+str(customer_id)+"'"
        conditionTr=conditionTr+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        
        conditionRsm=conditionRsm+"AND rep_id = '"+str(mso_id)+"'"
        conditionFm=conditionFm+"AND rep_id = '"+str(mso_id)+"'"
        conditionTr=conditionTr+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
        
        conditionRsm=conditionRsm+"AND market_id = '"+str(market_id)+"'"
        conditionFm=conditionFm+"AND market_id = '"+str(market_id)+"'"
        conditionTr=conditionTr+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
        
        conditionRsm=conditionRsm+"AND area_id = '"+str(teritory_id)+"'"
        conditionFm=conditionFm+"AND area_id = '"+str(teritory_id)+"'"
        conditionTr=conditionTr+"AND area_id = '"+str(teritory_id)+"'"
    
    records_S="SELECT  item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY item_id ORDER BY item_id;"
    records=db.executesql(records_S,as_dict = True) 
    
#     records=qset.select(db.sm_invoice.ALL,(db.sm_invoice.quantity * db.sm_invoice.actual_tp).sum(),(db.sm_invoice.quantity * db.sm_invoice.price).sum(),(db.sm_invoice.return_rate *db.sm_invoice.return_qty).sum(), groupby=db.sm_invoice.item_id, orderby=db.sm_invoice.item_name)
    
    records_rsmS="SELECT  level1_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND    invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionRsm+"  GROUP BY level1_id ORDER BY level1_id;"
    records_fpS="SELECT  level2_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionFm+"  GROUP BY level2_id ORDER BY level2_id;"
    records_trS="SELECT  level3_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionTr+"  GROUP BY level3_id ORDER BY level3_id;"
#     return records_trS
    records_rsm=db.executesql(records_rsmS,as_dict = True)
    records_fp=db.executesql(records_fpS,as_dict = True)
    records_tr=db.executesql(records_trS,as_dict = True)
    if records:
        return dict(records=records,records_rsm=records_rsm,records_tr=records_tr,records_fp=records_fp,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  teritory_id=teritory_id, teritory_name=teritory_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,page=page,items_per_page=items_per_page)
    
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
        
def productwiseSD():
    c_id=session.cid   
    response.title='Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()

    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    if (teritory_id==''):
        session.flash="Please select a Teritory"
        redirect(URL(c='report_sales',f='home'))
        
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    levelRows = db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == teritory_id)).select(db.sm_level.level1,db.sm_level.level2,limitby=(0,1))
    if levelRows:
        rsm=levelRows[0].level1
        fm=levelRows[0].level2
       

#     ===================
    condition=''
    conditionRsm=''
    conditionFm=''
    conditionTr=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
        
        conditionRsm=conditionRsm+"AND depot_id = '"+str(depot_id)+"'"
        conditionFm=conditionFm+"AND depot_id = '"+str(depot_id)+"'"
        conditionTr=conditionTr+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        
        conditionRsm=conditionRsm+"AND store_id = '"+str(store_id)+"'"
        conditionFm=conditionFm+"AND store_id = '"+str(store_id)+"'"
        conditionTr=conditionTr+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
        
        conditionRsm=conditionRsm+"AND client_id = '"+str(customer_id)+"'"
        conditionFm=conditionFm+"AND client_id = '"+str(customer_id)+"'"
        conditionTr=conditionTr+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        
        conditionRsm=conditionRsm+"AND rep_id = '"+str(mso_id)+"'"
        conditionFm=conditionFm+"AND rep_id = '"+str(mso_id)+"'"
        conditionTr=conditionTr+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
        
        conditionRsm=conditionRsm+"AND market_id = '"+str(market_id)+"'"
        conditionFm=conditionFm+"AND market_id = '"+str(market_id)+"'"
        conditionTr=conditionTr+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
        
        conditionRsm=conditionRsm+"AND area_id = '"+str(teritory_id)+"'"
        conditionFm=conditionFm+"AND area_id = '"+str(teritory_id)+"'"
        conditionTr=conditionTr+"AND area_id = '"+str(teritory_id)+"'"
    
    records_S="SELECT  item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY item_id ORDER BY item_id;"
    records=db.executesql(records_S,as_dict = True) 
    
#     records=qset.select(db.sm_invoice.ALL,(db.sm_invoice.quantity * db.sm_invoice.actual_tp).sum(),(db.sm_invoice.quantity * db.sm_invoice.price).sum(),(db.sm_invoice.return_rate *db.sm_invoice.return_qty).sum(), groupby=db.sm_invoice.item_id, orderby=db.sm_invoice.item_name)
    
    records_rsmS="SELECT  level1_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND    invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionRsm+"  GROUP BY level1_id ORDER BY level1_id;"
    records_fpS="SELECT  level2_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionFm+"  GROUP BY level2_id ORDER BY level2_id;"
    records_trS="SELECT  level3_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionTr+"  GROUP BY level3_id ORDER BY level3_id;"
#     return records_trS
    records_rsm=db.executesql(records_rsmS,as_dict = True)
    records_fp=db.executesql(records_fpS,as_dict = True)
    records_tr=db.executesql(records_trS,as_dict = True)
    
    if records:
        myString='DateRange,'+date_from+','+date_to+'\n'
        myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString+='Store,'+store_id+'|'+store_name+'\n'
        myString+='Area,'+teritory_id+'|'+teritory_name+'\n'
        myString+='Customer,'+customer_id+'|'+customer_name+'\n'
        myString+='MSO,'+mso_id+'|'+mso_name+'\n'
        myString+='Market,'+market_id+'|'+market_name+'\n\n'
        myString=myString+',,Ret% ,InvioceQnty  ,  InvioceBonus  ,  InvioceTradePrice , ReturnQnty  ,  ReturnBonus  ,  ReturnTradePrice  , NetQnty ,   NetBonus  ,  NetTradePrice\n'
        
        for i in range(len(records_rsm)):
            record_rsm=records_rsm[i]
            netSoldRsm=record_rsm['actual_tp']-record_rsm['retTP']
            saleRsm=record_rsm['actual_tp']
            rSaleRsm=record_rsm['retTP']
            rPRsm=0
            if (rSaleRsm > 0):
                rPRsm=(rSaleRsm*100)/saleRsm
            myString=myString+'RSM,'+str(record_rsm['level1_id'])+','+str(rPRsm)+','+str(record_rsm['inv_qty'])+','+str(record_rsm['inv_bonus_qty'])+','+str(record_rsm['actual_tp'])+','+str(record_rsm['ret_qty'])+','+str(record_rsm['ret_bonus_qty'])+','+ str(record_rsm['retTP'])+',' +str(record_rsm['inv_qty']-record_rsm['ret_qty'])+','+str(record_rsm['inv_bonus_qty']-record_rsm['ret_bonus_qty'])+','+str(netSoldRsm)+'\n'                           
        for i in range(len(records_fp)):
            record_fp=records_fp[i]
            netSoldFp=record_fp['actual_tp']-record_fp['retTP']
            saleFp=record_fp['actual_tp']
            rSaleFp=record_fp['retTP']
            rPFp=0
            if (rSaleFp > 0):
                rPFp=(rSaleFp*100)/saleFp
            myString=myString+'FM,'+str(record_fp['level2_id'])+','+str(rPFp)+','+str(record_fp['inv_qty'])+','+str(record_fp['inv_bonus_qty'])+','+str(record_fp['actual_tp'])+','+str(record_fp['ret_qty'])+','+str(record_fp['ret_bonus_qty'])+','+ str(record_fp['retTP'])+',' +str(record_fp['inv_qty']-record_fp['ret_qty'])+','+str(record_fp['inv_bonus_qty']-record_fp['ret_bonus_qty'])+','+str(netSoldFp)+'\n'                                 
        
        for i in range(len(records_tr)):
            record_tr=records_tr[i]
            netSoldTr=record_tr['actual_tp']-record_tr['retTP']
            saleTr=record_tr['actual_tp']
            rSaleTr=record_tr['retTP']
            rPTr=0
            if (rSaleTr > 0):
                rPTr=(rSaleTr*100)/saleTr
# 
            myString=myString+'TR,'+str(record_tr['level3_id'])+','+str(rPTr)+','+str(record_tr['inv_qty'])+','+str(record_tr['inv_bonus_qty'])+','+str(record_tr['actual_tp'])+','+str(record_tr['ret_qty'])+','+str(record_tr['ret_bonus_qty'])+','+ str(record_tr['retTP'])+',' +str(record_tr['inv_qty']-record_tr['ret_qty'])+','+str(record_tr['inv_bonus_qty']-record_tr['ret_bonus_qty'])+','+str(netSoldTr)+'\n'                                 
        
        myString =myString+ 'ItemID ,   ItemName  ,  UOM   , UnitPrice ,   Ret% ,  InvioceQnty  ,  InvioceBonus  ,  InvioceTradePrice   ,  ReturnQnty  ,  ReturnBonus  ,  ReturnTradePrice  ,  NetQnty  ,  NetBonus  ,  NetTradePrice \n' 
                            
        for i in range(len(records)):
            record=records[i]
            netSold=record['actual_tp']-record['retTP']
            sale=record['actual_tp']
            rSale=record['retTP']
            rP=0
            if (rSale > 0):
                rP=(rSale*100)/sale
            myString=myString+str(record['item_id'])+','+str(record['item_name'])+','+str(record['item_unit'])+','+str(record['unitTP'])+','+str(round(rP,2))+','+str(rP)+','+str(record['inv_qty'])+','+str(record['inv_bonus_qty'])+','+str(record['actual_tp'])+','+str(record['ret_qty'])+','+str(record['ret_bonus_qty'])+','+str(record['retTP'])+','+str(record['inv_qty']-record['ret_qty'])+','+str(record['inv_bonus_qty']-record['ret_bonus_qty'])+','+str(netSold)+'\n'
            
    
    
        #Save as csv
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=ProductWiseSalesStatement.csv'   
        return str(myString)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
        
# ========================================
def productwiseSwithoutBonus():   
    c_id=session.cid   
    response.title='Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()

    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    if (teritory_id==''):
        session.flash="Please select a Teritory"
        redirect(URL(c='report_sales',f='home'))
        
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    levelRows = db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == teritory_id)).select(db.sm_level.level1,db.sm_level.level2,limitby=(0,1))
    if levelRows:
        rsm=levelRows[0].level1
        fm=levelRows[0].level2
       

#     ===================
    condition=''
    conditionRsm=''
    conditionFm=''
    conditionTr=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
        
        conditionRsm=conditionRsm+"AND depot_id = '"+str(depot_id)+"'"
        conditionFm=conditionFm+"AND depot_id = '"+str(depot_id)+"'"
        conditionTr=conditionTr+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        
        conditionRsm=conditionRsm+"AND store_id = '"+str(store_id)+"'"
        conditionFm=conditionFm+"AND store_id = '"+str(store_id)+"'"
        conditionTr=conditionTr+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
        
        conditionRsm=conditionRsm+"AND client_id = '"+str(customer_id)+"'"
        conditionFm=conditionFm+"AND client_id = '"+str(customer_id)+"'"
        conditionTr=conditionTr+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        
        conditionRsm=conditionRsm+"AND rep_id = '"+str(mso_id)+"'"
        conditionFm=conditionFm+"AND rep_id = '"+str(mso_id)+"'"
        conditionTr=conditionTr+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
        
        conditionRsm=conditionRsm+"AND market_id = '"+str(market_id)+"'"
        conditionFm=conditionFm+"AND market_id = '"+str(market_id)+"'"
        conditionTr=conditionTr+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
        
        conditionRsm=conditionRsm+"AND area_id = '"+str(teritory_id)+"'"
        conditionFm=conditionFm+"AND area_id = '"+str(teritory_id)+"'"
        conditionTr=conditionTr+"AND area_id = '"+str(teritory_id)+"'"
    
    records_S="SELECT  item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty = 0 AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY item_id ORDER BY item_id;"
    records=db.executesql(records_S,as_dict = True) 
    
#     records=qset.select(db.sm_invoice.ALL,(db.sm_invoice.quantity * db.sm_invoice.actual_tp).sum(),(db.sm_invoice.quantity * db.sm_invoice.price).sum(),(db.sm_invoice.return_rate *db.sm_invoice.return_qty).sum(), groupby=db.sm_invoice.item_id, orderby=db.sm_invoice.item_name)
    
    records_rsmS="SELECT  level1_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty = 0 AND    invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionRsm+"  GROUP BY level1_id ORDER BY level1_id;"
    records_fpS="SELECT  level2_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty = 0 AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionFm+"  GROUP BY level2_id ORDER BY level2_id;"
    records_trS="SELECT  level3_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty = 0 AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionTr+"  GROUP BY level3_id ORDER BY level3_id;"
#     return records_trS
    records_rsm=db.executesql(records_rsmS,as_dict = True)
    records_fp=db.executesql(records_fpS,as_dict = True)
    records_tr=db.executesql(records_trS,as_dict = True)
    if records:
        return dict(records=records,records_rsm=records_rsm,records_tr=records_tr,records_fp=records_fp,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  teritory_id=teritory_id, teritory_name=teritory_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,page=page,items_per_page=items_per_page)
    
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))

def productwiseSwithoutBonusD():   
    c_id=session.cid   
    response.title='Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()

    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    if (teritory_id==''):
        session.flash="Please select a Teritory"
        redirect(URL(c='report_sales',f='home'))
        
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    levelRows = db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == teritory_id)).select(db.sm_level.level1,db.sm_level.level2,limitby=(0,1))
    if levelRows:
        rsm=levelRows[0].level1
        fm=levelRows[0].level2
       

#     ===================
    condition=''
    conditionRsm=''
    conditionFm=''
    conditionTr=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
        
        conditionRsm=conditionRsm+"AND depot_id = '"+str(depot_id)+"'"
        conditionFm=conditionFm+"AND depot_id = '"+str(depot_id)+"'"
        conditionTr=conditionTr+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        
        conditionRsm=conditionRsm+"AND store_id = '"+str(store_id)+"'"
        conditionFm=conditionFm+"AND store_id = '"+str(store_id)+"'"
        conditionTr=conditionTr+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
        
        conditionRsm=conditionRsm+"AND client_id = '"+str(customer_id)+"'"
        conditionFm=conditionFm+"AND client_id = '"+str(customer_id)+"'"
        conditionTr=conditionTr+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        
        conditionRsm=conditionRsm+"AND rep_id = '"+str(mso_id)+"'"
        conditionFm=conditionFm+"AND rep_id = '"+str(mso_id)+"'"
        conditionTr=conditionTr+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
        
        conditionRsm=conditionRsm+"AND market_id = '"+str(market_id)+"'"
        conditionFm=conditionFm+"AND market_id = '"+str(market_id)+"'"
        conditionTr=conditionTr+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
        
        conditionRsm=conditionRsm+"AND area_id = '"+str(teritory_id)+"'"
        conditionFm=conditionFm+"AND area_id = '"+str(teritory_id)+"'"
        conditionTr=conditionTr+"AND area_id = '"+str(teritory_id)+"'"
    
    records_S="SELECT  item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty = 0 AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY item_id ORDER BY item_id;"
    records=db.executesql(records_S,as_dict = True) 
    
#     records=qset.select(db.sm_invoice.ALL,(db.sm_invoice.quantity * db.sm_invoice.actual_tp).sum(),(db.sm_invoice.quantity * db.sm_invoice.price).sum(),(db.sm_invoice.return_rate *db.sm_invoice.return_qty).sum(), groupby=db.sm_invoice.item_id, orderby=db.sm_invoice.item_name)
    
    records_rsmS="SELECT  level1_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty = 0 AND    invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionRsm+"  GROUP BY level1_id ORDER BY level1_id;"
    records_fpS="SELECT  level2_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty = 0 AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionFm+"  GROUP BY level2_id ORDER BY level2_id;"
    records_trS="SELECT  level3_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty = 0 AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionTr+"  GROUP BY level3_id ORDER BY level3_id;"
#     return records_trS
    records_rsm=db.executesql(records_rsmS,as_dict = True)
    records_fp=db.executesql(records_fpS,as_dict = True)
    records_tr=db.executesql(records_trS,as_dict = True)
    
    if records:
        myString='DateRange,'+date_from+','+date_to+'\n'
        myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString+='Store,'+store_id+'|'+store_name+'\n'
        myString+='Area,'+teritory_id+'|'+teritory_name+'\n'
        myString+='Customer,'+customer_id+'|'+customer_name+'\n'
        myString+='MSO,'+mso_id+'|'+mso_name+'\n'
        myString+='Market,'+market_id+'|'+market_name+'\n\n'
        myString=myString+',,Ret% ,InvioceQnty  ,  InvioceBonus  ,  InvioceTradePrice , ReturnQnty  ,  ReturnBonus  ,  ReturnTradePrice  , NetQnty ,   NetBonus  ,  NetTradePrice\n'
        
        for i in range(len(records_rsm)):
            record_rsm=records_rsm[i]
            netSoldRsm=record_rsm['actual_tp']-record_rsm['retTP']
            saleRsm=record_rsm['actual_tp']
            rSaleRsm=record_rsm['retTP']
            rPRsm=0
            if (rSaleRsm > 0):
                rPRsm=(rSaleRsm*100)/saleRsm
            myString=myString+'RSM,'+str(record_rsm['level1_id'])+','+str(rPRsm)+','+str(record_rsm['inv_qty'])+','+str(record_rsm['inv_bonus_qty'])+','+str(record_rsm['actual_tp'])+','+str(record_rsm['ret_qty'])+','+str(record_rsm['ret_bonus_qty'])+','+ str(record_rsm['retTP'])+',' +str(record_rsm['inv_qty']-record_rsm['ret_qty'])+','+str(record_rsm['inv_bonus_qty']-record_rsm['ret_bonus_qty'])+','+str(netSoldRsm)+'\n'                           
        for i in range(len(records_fp)):
            record_fp=records_fp[i]
            netSoldFp=record_fp['actual_tp']-record_fp['retTP']
            saleFp=record_fp['actual_tp']
            rSaleFp=record_fp['retTP']
            rPFp=0
            if (rSaleFp > 0):
                rPFp=(rSaleFp*100)/saleFp
            myString=myString+'FM,'+str(record_fp['level2_id'])+','+str(rPFp)+','+str(record_fp['inv_qty'])+','+str(record_fp['inv_bonus_qty'])+','+str(record_fp['actual_tp'])+','+str(record_fp['ret_qty'])+','+str(record_fp['ret_bonus_qty'])+','+ str(record_fp['retTP'])+',' +str(record_fp['inv_qty']-record_fp['ret_qty'])+','+str(record_fp['inv_bonus_qty']-record_fp['ret_bonus_qty'])+','+str(netSoldFp)+'\n'                                 
        
        for i in range(len(records_tr)):
            record_tr=records_tr[i]
            netSoldTr=record_tr['actual_tp']-record_tr['retTP']
            saleTr=record_tr['actual_tp']
            rSaleTr=record_tr['retTP']
            rPTr=0
            if (rSaleTr > 0):
                rPTr=(rSaleTr*100)/saleTr
# 
            myString=myString+'TR,'+str(record_tr['level3_id'])+','+str(rPTr)+','+str(record_tr['inv_qty'])+','+str(record_tr['inv_bonus_qty'])+','+str(record_tr['actual_tp'])+','+str(record_tr['ret_qty'])+','+str(record_tr['ret_bonus_qty'])+','+ str(record_tr['retTP'])+',' +str(record_tr['inv_qty']-record_tr['ret_qty'])+','+str(record_tr['inv_bonus_qty']-record_tr['ret_bonus_qty'])+','+str(netSoldTr)+'\n'                                 
        
        myString =myString+ 'ItemID ,   ItemName  ,  UOM   , UnitPrice ,   Ret% ,  InvioceQnty  ,  InvioceBonus  ,  InvioceTradePrice   ,  ReturnQnty  ,  ReturnBonus  ,  ReturnTradePrice  ,  NetQnty  ,  NetBonus  ,  NetTradePrice \n' 
                            
        for i in range(len(records)):
            record=records[i]
            netSold=record['actual_tp']-record['retTP']
            sale=record['actual_tp']
            rSale=record['retTP']
            rP=0
            if (rSale > 0):
                rP=(rSale*100)/sale
            myString=myString+str(record['item_id'])+','+str(record['item_name'])+','+str(record['item_unit'])+','+str(record['unitTP'])+','+str(round(rP,2))+','+str(rP)+','+str(record['inv_qty'])+','+str(record['inv_bonus_qty'])+','+str(record['actual_tp'])+','+str(record['ret_qty'])+','+str(record['ret_bonus_qty'])+','+str(record['retTP'])+','+str(record['inv_qty']-record['ret_qty'])+','+str(record['inv_bonus_qty']-record['ret_bonus_qty'])+','+str(netSold)+'\n'
            
    
    
        #Save as csv
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=ProductWiseSalesStatementWithoutBonus.csv'   
        return str(myString)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))

# ==================================       
def customrInvoiceProductwiseS():
    c_id=session.cid   
    response.title='Customer-Invoice-Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()

    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    if (teritory_id==''):
        session.flash="Please select a Teritory"
        redirect(URL(c='report_sales',f='home'))
        
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    levelRows = db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == teritory_id)).select(db.sm_level.level1,db.sm_level.level2,limitby=(0,1))
    if levelRows:
        rsm=levelRows[0].level1
        fm=levelRows[0].level2
        
    
    condition=''
    condition_head=''
    conditionRsm=''
    conditionFm=''
    conditionTr=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
        condition_head=condition_head+"AND depot_id = '"+str(depot_id)+"'"
        
        conditionRsm=conditionRsm+"AND depot_id = '"+str(depot_id)+"'"
        conditionFm=conditionFm+"AND depot_id = '"+str(depot_id)+"'"
        conditionTr=conditionTr+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        condition_head=condition_head+"AND store_id = '"+str(store_id)+"'"
        
        conditionRsm=conditionRsm+"AND store_id = '"+str(store_id)+"'"
        conditionFm=conditionFm+"AND store_id = '"+str(store_id)+"'"
        conditionTr=conditionTr+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
        condition_head=condition_head+"AND client_id = '"+str(customer_id)+"'"
        
        conditionRsm=conditionRsm+"AND client_id = '"+str(customer_id)+"'"
        conditionFm=conditionFm+"AND client_id = '"+str(customer_id)+"'"
        conditionTr=conditionTr+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        condition_head=condition_head+"AND rep_id = '"+str(rep_id)+"'"
        
        conditionRsm=conditionRsm+"AND rep_id = '"+str(mso_id)+"'"
        conditionFm=conditionFm+"AND rep_id = '"+str(mso_id)+"'"
        conditionTr=conditionTr+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
        condition_head=condition_head+"AND market_id = '"+str(market_id)+"'"
        
        conditionRsm=conditionRsm+"AND market_id = '"+str(market_id)+"'"
        conditionFm=conditionFm+"AND market_id = '"+str(market_id)+"'"
        conditionTr=conditionTr+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
        condition_head=condition_head+"AND area_id = '"+str(teritory_id)+"'"
        
        conditionRsm=conditionRsm+"AND area_id = '"+str(teritory_id)+"'"
        conditionFm=conditionFm+"AND area_id = '"+str(teritory_id)+"'"
        conditionTr=conditionTr+"AND area_id = '"+str(teritory_id)+"'"
        
    records_S="SELECT  depot_id,invoice_date,area_name,sl,client_id,client_name,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY client_id,sl ORDER BY client_id,sl;"
    records=db.executesql(records_S,as_dict = True) 
    recordshead_S="SELECT  sl,client_id,client_name,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY client_id,sl ORDER BY client_id,sl;"
#     return recordshead_S
    records_head=db.executesql(recordshead_S,as_dict = True) 
    
    
    records_rsmS="SELECT  level1_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionRsm+"  GROUP BY level1_id ORDER BY level1_id;"
    records_fpS="SELECT  level2_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionFm+"  GROUP BY level2_id ORDER BY level2_id;"
    records_trS="SELECT  level3_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionTr+"  GROUP BY level3_id ORDER BY level3_id;"

    records_rsm=db.executesql(records_rsmS,as_dict = True)
    records_fp=db.executesql(records_fpS,as_dict = True)
    records_tr=db.executesql(records_trS,as_dict = True)
    
        
    if records:
        reportHeadDict={}
        reportHeadList=[]
        InvSlList=[] 
#         return len(records_head)
        for i in range(len(records_head)):
            
            head_sl=records_head[i]['sl']
            head_client=records_head[i]['client_id']
            head_qty=records_head[i]['inv_qty']
            head_Bonusqty=records_head[i]['inv_bonus_qty']
            head_ret_qty=records_head[i]['ret_qty']
            head_ret_bonus_qty=records_head[i]['ret_bonus_qty']
            head_check=str(head_sl)+'-'+str(head_client)
            
            head_invTotal=records_head[i]['actual_tp']
            head_retTotal=records_head[i]['retTP']
            reportHeadDict={'head_sl':head_sl,'head_qty':head_qty,'head_Bonusqty':head_Bonusqty,'head_ret_qty':head_ret_qty,'head_ret_bonus_qty':head_ret_bonus_qty,'head_invTotal':head_invTotal,'head_retTotal':head_retTotal}
            
            
            reportHeadList.append(reportHeadDict)
            InvSlList.append(head_check)
        
        
        
        
        return dict(records=records,reportHeadList=reportHeadList,InvSlList=InvSlList,records_rsm=records_rsm,records_tr=records_tr,records_fp=records_fp,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  teritory_id=teritory_id, teritory_name=teritory_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,page=page,items_per_page=items_per_page)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
        
        
def customrInvoiceProductwiseSD():
    c_id=session.cid   
    response.title='Customer-Invoice-Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()

    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    if (teritory_id==''):
        session.flash="Please select a Teritory"
        redirect(URL(c='report_sales',f='home'))
        
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    levelRows = db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == teritory_id)).select(db.sm_level.level1,db.sm_level.level2,limitby=(0,1))
    if levelRows:
        rsm=levelRows[0].level1
        fm=levelRows[0].level2
        
    
    condition=''
    condition_head=''
#     conditionRsm=''
#     conditionFm=''
#     conditionTr=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
        condition_head=condition_head+"AND depot_id = '"+str(depot_id)+"'"
        
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        condition_head=condition_head+"AND store_id = '"+str(store_id)+"'"
        
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
        condition_head=condition_head+"AND client_id = '"+str(customer_id)+"'"

    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        condition_head=condition_head+"AND rep_id = '"+str(rep_id)+"'"

    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
        condition_head=condition_head+"AND market_id = '"+str(market_id)+"'"

    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
        condition_head=condition_head+"AND area_id = '"+str(teritory_id)+"'"

        
    records_S="SELECT  depot_id,invoice_date,area_name,sl,client_id,client_name,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY client_id,sl ORDER BY client_id,sl;"
    records=db.executesql(records_S,as_dict = True) 
    recordshead_S="SELECT  sl,client_id,client_name,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY client_id,sl ORDER BY client_id,sl;"
#     return recordshead_S
    records_head=db.executesql(recordshead_S,as_dict = True) 
        
    if records:
        reportHeadDict={}
        reportHeadList=[]
        InvSlList=[] 
#         return len(records_head)
        for i in range(len(records_head)):
            
            head_sl=records_head[i]['sl']
            head_client=records_head[i]['client_id']
            head_qty=records_head[i]['inv_qty']
            head_Bonusqty=records_head[i]['inv_bonus_qty']
            head_ret_qty=records_head[i]['ret_qty']
            head_ret_bonus_qty=records_head[i]['ret_bonus_qty']
            head_check=str(head_sl)+'-'+str(head_client)
            
            head_invTotal=records_head[i]['actual_tp']
            head_retTotal=records_head[i]['retTP']
            reportHeadDict={'head_sl':head_sl,'head_qty':head_qty,'head_Bonusqty':head_Bonusqty,'head_ret_qty':head_ret_qty,'head_ret_bonus_qty':head_ret_bonus_qty,'head_invTotal':head_invTotal,'head_retTotal':head_retTotal}
            
            
            reportHeadList.append(reportHeadDict)
            InvSlList.append(head_check)        

        myString = '\nClientID,ClientName,Inv,InvDate,AreaName,HeadInvTotal,HeadRetTotal,HeadTotal,ItemID ,   ItemName  ,  UOM  ,  UnitPrice ,   Ret% , InvioceQnty  ,  InvioceBonus  ,  InvioceTradePrice ,ReturnQnty   , ReturnBonus  ,  ReturnTradePrice ,NetQnty  ,  NetBonus ,   NetTradePrice \n'
        p=0
        clientID=''
        invsl=''
        
        for i in range(len(records)):
            record=records[i]
            head_check=str(record['sl'])+'-'+str(record['client_id']) 
            if [s for s in InvSlList if head_check in s]:
              index_element = InvSlList.index(head_check)           
              head_data=reportHeadList[index_element] 

                
            netSold=record['actual_tp']-record['retTP']
            sale=record['actual_tp']
            rSale=record['retTP']
            rP=0
            if (rSale > 0):
                rP=(rSale*100)/sale
            myString =myString+str(record['client_id'])+',' +str(record['client_name'])+','
            myString =myString+'INV'+str(record['depot_id'])+str(record['sl'])+','+str(record['invoice_date']) +','+str(record['area_name'])   +','+str(head_data['head_invTotal'])+','+ str(head_data['head_retTotal']) +',' +str(float(head_data['head_invTotal'])-float(head_data['head_retTotal'])) +','
            myString=myString+str(record['item_id'])+','+str(record['item_name'])+','+str(record['item_unit'])+','+str(record['actual_tp'])+','+str(rP)+','+str(record['inv_qty'])+','+str(record['inv_bonus_qty'])+','+str(record['actual_tp'])+','+str(record['ret_qty'])+','+str(record['ret_bonus_qty'])+','+str(record['retTP'])+','+str(record['inv_qty']-record['ret_qty'])+','+str(record['inv_bonus_qty']-record['ret_bonus_qty'])+','+str(netSold)+'\n'
            clientID=record['client_id']
        
        #Save as csv
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=CustomerInvoiceProductWiseSalesStatement.csv'   
        return str(myString)
        
        
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))   
#  =========================================================   
def customrInvoiceProductwiseSwithBonus():
    
    c_id=session.cid   
    response.title='Customer-Invoice-Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()

    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    if (teritory_id==''):
        session.flash="Please select a Teritory"
        redirect(URL(c='report_sales',f='home'))
        
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    levelRows = db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == teritory_id)).select(db.sm_level.level1,db.sm_level.level2,limitby=(0,1))
    if levelRows:
        rsm=levelRows[0].level1
        fm=levelRows[0].level2
        
    
    
    
    condition=''
    condition_head=''
    conditionRsm=''
    conditionFm=''
    conditionTr=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
        condition_head=condition_head+"AND depot_id = '"+str(depot_id)+"'"
        
        conditionRsm=conditionRsm+"AND depot_id = '"+str(depot_id)+"'"
        conditionFm=conditionFm+"AND depot_id = '"+str(depot_id)+"'"
        conditionTr=conditionTr+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        condition_head=condition_head+"AND store_id = '"+str(store_id)+"'"
        
        conditionRsm=conditionRsm+"AND store_id = '"+str(store_id)+"'"
        conditionFm=conditionFm+"AND store_id = '"+str(store_id)+"'"
        conditionTr=conditionTr+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
        condition_head=condition_head+"AND client_id = '"+str(customer_id)+"'"
        
        conditionRsm=conditionRsm+"AND client_id = '"+str(customer_id)+"'"
        conditionFm=conditionFm+"AND client_id = '"+str(customer_id)+"'"
        conditionTr=conditionTr+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        condition_head=condition_head+"AND rep_id = '"+str(rep_id)+"'"
        
        conditionRsm=conditionRsm+"AND rep_id = '"+str(mso_id)+"'"
        conditionFm=conditionFm+"AND rep_id = '"+str(mso_id)+"'"
        conditionTr=conditionTr+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
        condition_head=condition_head+"AND market_id = '"+str(market_id)+"'"
        
        conditionRsm=conditionRsm+"AND market_id = '"+str(market_id)+"'"
        conditionFm=conditionFm+"AND market_id = '"+str(market_id)+"'"
        conditionTr=conditionTr+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
        condition_head=condition_head+"AND area_id = '"+str(teritory_id)+"'"
        
        conditionRsm=conditionRsm+"AND area_id = '"+str(teritory_id)+"'"
        conditionFm=conditionFm+"AND area_id = '"+str(teritory_id)+"'"
        conditionTr=conditionTr+"AND area_id = '"+str(teritory_id)+"'"
        
    records_S="SELECT  depot_id,invoice_date,area_name,sl,client_id,client_name,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty > 0 AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY client_id,sl ORDER BY client_id,sl;"
    records=db.executesql(records_S,as_dict = True) 
    recordshead_S="SELECT  sl,client_id,client_name,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty > 0 AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY client_id,sl ORDER BY client_id,sl;"
#     return recordshead_S
    records_head=db.executesql(recordshead_S,as_dict = True) 
    
    
    records_rsmS="SELECT  level1_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty > 0 AND    invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionRsm+"  GROUP BY level1_id ORDER BY level1_id;"
    records_fpS="SELECT  level2_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty > 0 AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionFm+"  GROUP BY level2_id ORDER BY level2_id;"
    records_trS="SELECT  level3_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty > 0 AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionTr+"  GROUP BY level3_id ORDER BY level3_id;"

    records_rsm=db.executesql(records_rsmS,as_dict = True)
    records_fp=db.executesql(records_fpS,as_dict = True)
    records_tr=db.executesql(records_trS,as_dict = True)
    
        
    if records:
        reportHeadDict={}
        reportHeadList=[]
        InvSlList=[] 
#         return len(records_head)
        for i in range(len(records_head)):
            head_sl=records_head[i]['sl']
            head_client=records_head[i]['client_id']
            head_qty=records_head[i]['inv_qty']
            head_Bonusqty=records_head[i]['inv_bonus_qty']
            head_ret_qty=records_head[i]['ret_qty']
            head_ret_bonus_qty=records_head[i]['ret_bonus_qty']
            head_check=str(head_sl)+'-'+str(head_client)
            
            head_invTotal=records_head[i]['actual_tp']
            head_retTotal=records_head[i]['retTP']
            
            reportHeadDict={'head_sl':head_sl,'head_qty':head_qty,'head_Bonusqty':head_Bonusqty,'head_ret_qty':head_ret_qty,'head_ret_bonus_qty':head_ret_bonus_qty,'head_invTotal':head_invTotal,'head_retTotal':head_retTotal}  
            reportHeadList.append(reportHeadDict)
            InvSlList.append(head_check)

        return dict(records=records,reportHeadList=reportHeadList,InvSlList=InvSlList,records_rsm=records_rsm,records_tr=records_tr,records_fp=records_fp,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  teritory_id=teritory_id, teritory_name=teritory_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,page=page,items_per_page=items_per_page)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
        
def customrInvoiceProductwiseSwithBonusD():
    c_id=session.cid   
    response.title='Customer-Invoice-Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()

    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    if (teritory_id==''):
        session.flash="Please select a Teritory"
        redirect(URL(c='report_sales',f='home'))
        
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    levelRows = db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == teritory_id)).select(db.sm_level.level1,db.sm_level.level2,limitby=(0,1))
    if levelRows:
        rsm=levelRows[0].level1
        fm=levelRows[0].level2
        
    
    condition=''
    condition_head=''
#     conditionRsm=''
#     conditionFm=''
#     conditionTr=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
        condition_head=condition_head+"AND depot_id = '"+str(depot_id)+"'"
        
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        condition_head=condition_head+"AND store_id = '"+str(store_id)+"'"
        
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
        condition_head=condition_head+"AND client_id = '"+str(customer_id)+"'"

    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        condition_head=condition_head+"AND rep_id = '"+str(rep_id)+"'"

    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
        condition_head=condition_head+"AND market_id = '"+str(market_id)+"'"

    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
        condition_head=condition_head+"AND area_id = '"+str(teritory_id)+"'"

        
    records_S="SELECT  depot_id,invoice_date,area_name,sl,client_id,client_name,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty > 0 AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY client_id,sl ORDER BY client_id,sl;"
    records=db.executesql(records_S,as_dict = True) 
    recordshead_S="SELECT  sl,client_id,client_name,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty > 0 AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY client_id,sl ORDER BY client_id,sl;"
#     return recordshead_S
    records_head=db.executesql(recordshead_S,as_dict = True) 
        
    if records:
        reportHeadDict={}
        reportHeadList=[]
        InvSlList=[] 
#         return len(records_head)
        for i in range(len(records_head)):
            
            head_sl=records_head[i]['sl']
            head_client=records_head[i]['client_id']
            head_qty=records_head[i]['inv_qty']
            head_Bonusqty=records_head[i]['inv_bonus_qty']
            head_ret_qty=records_head[i]['ret_qty']
            head_ret_bonus_qty=records_head[i]['ret_bonus_qty']
            head_check=str(head_sl)+'-'+str(head_client)
            
            head_invTotal=records_head[i]['actual_tp']
            head_retTotal=records_head[i]['retTP']
            reportHeadDict={'head_sl':head_sl,'head_qty':head_qty,'head_Bonusqty':head_Bonusqty,'head_ret_qty':head_ret_qty,'head_ret_bonus_qty':head_ret_bonus_qty,'head_invTotal':head_invTotal,'head_retTotal':head_retTotal}
            
            
            reportHeadList.append(reportHeadDict)
            InvSlList.append(head_check)        

        myString = '\nClientID,ClientName,Inv,InvDate,AreaName,HeadInvTotal,HeadRetTotal,HeadTotal,ItemID ,   ItemName  ,  UOM  ,  UnitPrice ,   Ret% , InvioceQnty  ,  InvioceBonus  ,  InvioceTradePrice ,ReturnQnty   , ReturnBonus  ,  ReturnTradePrice ,NetQnty  ,  NetBonus ,   NetTradePrice \n'
        p=0
        clientID=''
        invsl=''
        
        for i in range(len(records)):
            record=records[i]
            head_check=str(record['sl'])+'-'+str(record['client_id']) 
            if [s for s in InvSlList if head_check in s]:
              index_element = InvSlList.index(head_check)           
              head_data=reportHeadList[index_element] 

                
            netSold=record['actual_tp']-record['retTP']
            sale=record['actual_tp']
            rSale=record['retTP']
            rP=0
            if (rSale > 0):
                rP=(rSale*100)/sale
            myString =myString+str(record['client_id'])+',' +str(record['client_name'])+','
            myString =myString+'INV'+str(record['depot_id'])+str(record['sl'])+','+str(record['invoice_date']) +','+str(record['area_name'])   +','+str(head_data['head_invTotal'])+','+ str(head_data['head_retTotal']) +',' +str(float(head_data['head_invTotal'])-float(head_data['head_retTotal'])) +','
            myString=myString+str(record['item_id'])+','+str(record['item_name'])+','+str(record['item_unit'])+','+str(record['actual_tp'])+','+str(rP)+','+str(record['inv_qty'])+','+str(record['inv_bonus_qty'])+','+str(record['actual_tp'])+','+str(record['ret_qty'])+','+str(record['ret_bonus_qty'])+','+str(record['retTP'])+','+str(record['inv_qty']-record['ret_qty'])+','+str(record['inv_bonus_qty']-record['ret_bonus_qty'])+','+str(netSold)+'\n'
            clientID=record['client_id']
        
        #Save as csv
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=CustomerInvoiceProductWiseSStatWithBonust.csv'   
        return str(myString)        
           
        
        
        
       
    else:
        
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))       
# =========================================================
        
def customrInvoiceProductwiseSwithoutBonus():
    
    c_id=session.cid   
    response.title='Customer-Invoice-Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()

    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    if (teritory_id==''):
        session.flash="Please select a Teritory"
        redirect(URL(c='report_sales',f='home'))
        
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    levelRows = db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == teritory_id)).select(db.sm_level.level1,db.sm_level.level2,limitby=(0,1))
    if levelRows:
        rsm=levelRows[0].level1
        fm=levelRows[0].level2
        
    condition=''
    condition_head=''
    conditionRsm=''
    conditionFm=''
    conditionTr=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
        condition_head=condition_head+"AND depot_id = '"+str(depot_id)+"'"
        
        conditionRsm=conditionRsm+"AND depot_id = '"+str(depot_id)+"'"
        conditionFm=conditionFm+"AND depot_id = '"+str(depot_id)+"'"
        conditionTr=conditionTr+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        condition_head=condition_head+"AND store_id = '"+str(store_id)+"'"
        
        conditionRsm=conditionRsm+"AND store_id = '"+str(store_id)+"'"
        conditionFm=conditionFm+"AND store_id = '"+str(store_id)+"'"
        conditionTr=conditionTr+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
        condition_head=condition_head+"AND client_id = '"+str(customer_id)+"'"
        
        conditionRsm=conditionRsm+"AND client_id = '"+str(customer_id)+"'"
        conditionFm=conditionFm+"AND client_id = '"+str(customer_id)+"'"
        conditionTr=conditionTr+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        condition_head=condition_head+"AND rep_id = '"+str(rep_id)+"'"
        
        conditionRsm=conditionRsm+"AND rep_id = '"+str(mso_id)+"'"
        conditionFm=conditionFm+"AND rep_id = '"+str(mso_id)+"'"
        conditionTr=conditionTr+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
        condition_head=condition_head+"AND market_id = '"+str(market_id)+"'"
        
        conditionRsm=conditionRsm+"AND market_id = '"+str(market_id)+"'"
        conditionFm=conditionFm+"AND market_id = '"+str(market_id)+"'"
        conditionTr=conditionTr+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
        condition_head=condition_head+"AND area_id = '"+str(teritory_id)+"'"
        
        conditionRsm=conditionRsm+"AND area_id = '"+str(teritory_id)+"'"
        conditionFm=conditionFm+"AND area_id = '"+str(teritory_id)+"'"
        conditionTr=conditionTr+"AND area_id = '"+str(teritory_id)+"'"
        
    records_S="SELECT  depot_id,invoice_date,area_name,sl,client_id,client_name,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty = 0 AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY client_id,sl ORDER BY client_id,sl;"
    records=db.executesql(records_S,as_dict = True) 
    recordshead_S="SELECT  sl,client_id,client_name,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty = 0 AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY client_id,sl ORDER BY client_id,sl;"
#     return recordshead_S
    records_head=db.executesql(recordshead_S,as_dict = True) 
    
    
    records_rsmS="SELECT  level1_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty = 0 AND    invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionRsm+"  GROUP BY level1_id ORDER BY level1_id;"
    records_fpS="SELECT  level2_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty = 0 AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionFm+"  GROUP BY level2_id ORDER BY level2_id;"
    records_trS="SELECT  level3_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty = 0 AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionTr+"  GROUP BY level3_id ORDER BY level3_id;"

    records_rsm=db.executesql(records_rsmS,as_dict = True)
    records_fp=db.executesql(records_fpS,as_dict = True)
    records_tr=db.executesql(records_trS,as_dict = True)
    
        
    if records:
        reportHeadDict={}
        reportHeadList=[]
        InvSlList=[] 
#         return len(records_head)
        for i in range(len(records_head)):
            head_sl=records_head[i]['sl']
            head_client=records_head[i]['client_id']
            head_qty=records_head[i]['inv_qty']
            head_Bonusqty=records_head[i]['inv_bonus_qty']
            head_ret_qty=records_head[i]['ret_qty']
            head_ret_bonus_qty=records_head[i]['ret_bonus_qty']
            head_check=str(head_sl)+'-'+str(head_client)
            
            head_invTotal=records_head[i]['actual_tp']
            head_retTotal=records_head[i]['retTP']
            
            reportHeadDict={'head_sl':head_sl,'head_qty':head_qty,'head_Bonusqty':head_Bonusqty,'head_ret_qty':head_ret_qty,'head_ret_bonus_qty':head_ret_bonus_qty,'head_invTotal':head_invTotal,'head_retTotal':head_retTotal}  
            reportHeadList.append(reportHeadDict)
            InvSlList.append(head_check)
        
        
        
        
        return dict(records=records,reportHeadList=reportHeadList,InvSlList=InvSlList,records_rsm=records_rsm,records_tr=records_tr,records_fp=records_fp,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  teritory_id=teritory_id, teritory_name=teritory_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,page=page,items_per_page=items_per_page)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
        
def customrInvoiceProductwiseSwithoutBonusD():
    c_id=session.cid   
    response.title='Customer-Invoice-Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()

    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    if (teritory_id==''):
        session.flash="Please select a Teritory"
        redirect(URL(c='report_sales',f='home'))
        
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    levelRows = db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == teritory_id)).select(db.sm_level.level1,db.sm_level.level2,limitby=(0,1))
    if levelRows:
        rsm=levelRows[0].level1
        fm=levelRows[0].level2
        
    
    condition=''
    condition_head=''
#     conditionRsm=''
#     conditionFm=''
#     conditionTr=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
        condition_head=condition_head+"AND depot_id = '"+str(depot_id)+"'"
        
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        condition_head=condition_head+"AND store_id = '"+str(store_id)+"'"
        
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
        condition_head=condition_head+"AND client_id = '"+str(customer_id)+"'"

    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        condition_head=condition_head+"AND rep_id = '"+str(rep_id)+"'"

    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
        condition_head=condition_head+"AND market_id = '"+str(market_id)+"'"

    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
        condition_head=condition_head+"AND area_id = '"+str(teritory_id)+"'"

        
    records_S="SELECT  depot_id,invoice_date,area_name,sl,client_id,client_name,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty = 0 AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY client_id,sl ORDER BY client_id,sl;"
    records=db.executesql(records_S,as_dict = True) 
    recordshead_S="SELECT  sl,client_id,client_name,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty = 0 AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY client_id,sl ORDER BY client_id,sl;"
#     return recordshead_S
    records_head=db.executesql(recordshead_S,as_dict = True) 
        
    if records:
        reportHeadDict={}
        reportHeadList=[]
        InvSlList=[] 
#         return len(records_head)
        for i in range(len(records_head)):
            
            head_sl=records_head[i]['sl']
            head_client=records_head[i]['client_id']
            head_qty=records_head[i]['inv_qty']
            head_Bonusqty=records_head[i]['inv_bonus_qty']
            head_ret_qty=records_head[i]['ret_qty']
            head_ret_bonus_qty=records_head[i]['ret_bonus_qty']
            head_check=str(head_sl)+'-'+str(head_client)
            
            head_invTotal=records_head[i]['actual_tp']
            head_retTotal=records_head[i]['retTP']
            reportHeadDict={'head_sl':head_sl,'head_qty':head_qty,'head_Bonusqty':head_Bonusqty,'head_ret_qty':head_ret_qty,'head_ret_bonus_qty':head_ret_bonus_qty,'head_invTotal':head_invTotal,'head_retTotal':head_retTotal}
            
            
            reportHeadList.append(reportHeadDict)
            InvSlList.append(head_check)        

        myString = '\nClientID,ClientName,Inv,InvDate,AreaName,HeadInvTotal,HeadRetTotal,HeadTotal,ItemID ,   ItemName  ,  UOM  ,  UnitPrice ,   Ret% , InvioceQnty  ,  InvioceBonus  ,  InvioceTradePrice ,ReturnQnty   , ReturnBonus  ,  ReturnTradePrice ,NetQnty  ,  NetBonus ,   NetTradePrice \n'
        p=0
        clientID=''
        invsl=''
        
        for i in range(len(records)):
            record=records[i]
            head_check=str(record['sl'])+'-'+str(record['client_id']) 
            if [s for s in InvSlList if head_check in s]:
              index_element = InvSlList.index(head_check)           
              head_data=reportHeadList[index_element] 

                
            netSold=record['actual_tp']-record['retTP']
            sale=record['actual_tp']
            rSale=record['retTP']
            rP=0
            if (rSale > 0):
                rP=(rSale*100)/sale
            myString =myString+str(record['client_id'])+',' +str(record['client_name'])+','
            myString =myString+'INV'+str(record['depot_id'])+str(record['sl'])+','+str(record['invoice_date']) +','+str(record['area_name'])   +','+str(head_data['head_invTotal'])+','+ str(head_data['head_retTotal']) +',' +str(float(head_data['head_invTotal'])-float(head_data['head_retTotal'])) +','
            myString=myString+str(record['item_id'])+','+str(record['item_name'])+','+str(record['item_unit'])+','+str(record['actual_tp'])+','+str(rP)+','+str(record['inv_qty'])+','+str(record['inv_bonus_qty'])+','+str(record['actual_tp'])+','+str(record['ret_qty'])+','+str(record['ret_bonus_qty'])+','+str(record['retTP'])+','+str(record['inv_qty']-record['ret_qty'])+','+str(record['inv_bonus_qty']-record['ret_bonus_qty'])+','+str(netSold)+'\n'
            clientID=record['client_id']
        
        #Save as csv
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=CustomerInvoiceProductWiseSStatWithoutBonust.csv'   
        return str(myString) 
        
    
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
# ================================
        
def productInvoicewiseSD():
    
    c_id=session.cid   
    response.title='Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
#     if (teritory_id==''):
#         session.flash="Please select a Teritory"
#         redirect(URL(c='report_sales',f='home'))
        
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    levelRows = db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == teritory_id)).select(db.sm_level.level1,db.sm_level.level2,limitby=(0,1))
    if levelRows:
        rsm=levelRows[0].level1
        fm=levelRows[0].level2
    
    condition=''
    condition_head=''
    conditionRsm=''
    conditionFm=''
    conditionTr=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
        condition_head=condition_head+"AND depot_id = '"+str(depot_id)+"'"
        
        conditionRsm=conditionRsm+"AND depot_id = '"+str(depot_id)+"'"
        conditionFm=conditionFm+"AND depot_id = '"+str(depot_id)+"'"
        conditionTr=conditionTr+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        condition_head=condition_head+"AND store_id = '"+str(store_id)+"'"
        
        conditionRsm=conditionRsm+"AND store_id = '"+str(store_id)+"'"
        conditionFm=conditionFm+"AND store_id = '"+str(store_id)+"'"
        conditionTr=conditionTr+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
        condition_head=condition_head+"AND client_id = '"+str(customer_id)+"'"
        
        conditionRsm=conditionRsm+"AND client_id = '"+str(customer_id)+"'"
        conditionFm=conditionFm+"AND client_id = '"+str(customer_id)+"'"
        conditionTr=conditionTr+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        condition_head=condition_head+"AND rep_id = '"+str(rep_id)+"'"
        
        conditionRsm=conditionRsm+"AND rep_id = '"+str(mso_id)+"'"
        conditionFm=conditionFm+"AND rep_id = '"+str(mso_id)+"'"
        conditionTr=conditionTr+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
        condition_head=condition_head+"AND market_id = '"+str(market_id)+"'"
        
        conditionRsm=conditionRsm+"AND market_id = '"+str(market_id)+"'"
        conditionFm=conditionFm+"AND market_id = '"+str(market_id)+"'"
        conditionTr=conditionTr+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
        condition_head=condition_head+"AND area_id = '"+str(teritory_id)+"'"
        
        conditionRsm=conditionRsm+"AND area_id = '"+str(teritory_id)+"'"
        conditionFm=conditionFm+"AND area_id = '"+str(teritory_id)+"'"
        conditionTr=conditionTr+"AND area_id = '"+str(teritory_id)+"'"
        
    records_S="SELECT  depot_id,invoice_date,area_name,sl,client_id,client_name,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY area_id,item_id ORDER BY area_id,item_id;"
    records=db.executesql(records_S,as_dict = True) 
    recordshead_S="SELECT  depot_id,sl,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY area_id,item_id ORDER BY area_id,item_id;"

    records_head=db.executesql(recordshead_S,as_dict = True) 
    
    
    records_rsmS="SELECT  level1_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND    invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionRsm+"  GROUP BY level1_id ORDER BY level1_id;"
    records_fpS="SELECT  level2_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionFm+"  GROUP BY level2_id ORDER BY level2_id;"
    records_trS="SELECT  level3_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionTr+"  GROUP BY level3_id ORDER BY level3_id;"

    records_rsm=db.executesql(records_rsmS,as_dict = True)
    records_fp=db.executesql(records_fpS,as_dict = True)
    records_tr=db.executesql(records_trS,as_dict = True)
    
    
    
    
    

#     return records
    if records:
        reportHeadDict={}
        reportHeadList=[]
        itemList=[] 
        for i in range(len(records_head)):
           head_item=records_head[i]['item_id']
           head_unit=records_head[i]['item_unit']
           head_price=records_head[i]['unitTP']
           head_qty=records_head[i]['inv_qty']
           head_Bonusqty=records_head[i]['inv_bonus_qty']
           head_ret_qty=records_head[i]['ret_qty']
           head_ret_bonus_qty=records_head[i]['ret_bonus_qty']

           head_invTotal=records_head[i]['actual_tp']
           head_retTotal=records_head[i]['retTP']
           reportHeadDict={'head_item':head_item,'head_unit':head_unit,'head_price':head_price,'head_qty':head_qty,'head_Bonusqty':head_Bonusqty,'head_ret_qty':head_ret_qty,'head_ret_bonus_qty':head_ret_bonus_qty,'head_invTotal':head_invTotal,'head_retTotal':head_retTotal}  
           reportHeadList.append(reportHeadDict)
           itemList.append(head_item)
        return dict(records=records,reportHeadList=reportHeadList,records_rsm=records_rsm,records_fp=records_fp,records_tr=records_tr,itemList=itemList,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  teritory_id=teritory_id, teritory_name=teritory_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,page=page,items_per_page=items_per_page)
    
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
        
        
# =====================================================
def productInvoicewiseSDD():
    c_id=session.cid   
    response.title='Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
#     if (teritory_id==''):
#         session.flash="Please select a Teritory"
#         redirect(URL(c='report_sales',f='home'))
        
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    levelRows = db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == teritory_id)).select(db.sm_level.level1,db.sm_level.level2,limitby=(0,1))
    if levelRows:
        rsm=levelRows[0].level1
        fm=levelRows[0].level2
    
    condition=''
    condition_head=''
    conditionRsm=''
    conditionFm=''
    conditionTr=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
        condition_head=condition_head+"AND depot_id = '"+str(depot_id)+"'"
        
        conditionRsm=conditionRsm+"AND depot_id = '"+str(depot_id)+"'"
        conditionFm=conditionFm+"AND depot_id = '"+str(depot_id)+"'"
        conditionTr=conditionTr+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        condition_head=condition_head+"AND store_id = '"+str(store_id)+"'"
        
        conditionRsm=conditionRsm+"AND store_id = '"+str(store_id)+"'"
        conditionFm=conditionFm+"AND store_id = '"+str(store_id)+"'"
        conditionTr=conditionTr+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
        condition_head=condition_head+"AND client_id = '"+str(customer_id)+"'"
        
        conditionRsm=conditionRsm+"AND client_id = '"+str(customer_id)+"'"
        conditionFm=conditionFm+"AND client_id = '"+str(customer_id)+"'"
        conditionTr=conditionTr+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        condition_head=condition_head+"AND rep_id = '"+str(rep_id)+"'"
        
        conditionRsm=conditionRsm+"AND rep_id = '"+str(mso_id)+"'"
        conditionFm=conditionFm+"AND rep_id = '"+str(mso_id)+"'"
        conditionTr=conditionTr+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
        condition_head=condition_head+"AND market_id = '"+str(market_id)+"'"
        
        conditionRsm=conditionRsm+"AND market_id = '"+str(market_id)+"'"
        conditionFm=conditionFm+"AND market_id = '"+str(market_id)+"'"
        conditionTr=conditionTr+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
        condition_head=condition_head+"AND area_id = '"+str(teritory_id)+"'"
        
        conditionRsm=conditionRsm+"AND area_id = '"+str(teritory_id)+"'"
        conditionFm=conditionFm+"AND area_id = '"+str(teritory_id)+"'"
        conditionTr=conditionTr+"AND area_id = '"+str(teritory_id)+"'"
        
    records_S="SELECT  depot_id,invoice_date,area_name,sl,client_id,client_name,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY area_id,item_id ORDER BY area_id,item_id;"
    records=db.executesql(records_S,as_dict = True) 
    recordshead_S="SELECT  depot_id,sl,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY area_id,item_id ORDER BY area_id,item_id;"

    records_head=db.executesql(recordshead_S,as_dict = True) 
    
    
    records_rsmS="SELECT  level1_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND    invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionRsm+"  GROUP BY level1_id ORDER BY level1_id;"
    records_fpS="SELECT  level2_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionFm+"  GROUP BY level2_id ORDER BY level2_id;"
    records_trS="SELECT  level3_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionTr+"  GROUP BY level3_id ORDER BY level3_id;"

    records_rsm=db.executesql(records_rsmS,as_dict = True)
    records_fp=db.executesql(records_fpS,as_dict = True)
    records_tr=db.executesql(records_trS,as_dict = True)
    
    
    
    
    

#     return records
    if records:
        reportHeadDict={}
        reportHeadList=[]
        itemList=[] 
        for i in range(len(records_head)):
           head_item=records_head[i]['item_id']
           head_unit=records_head[i]['item_unit']
           head_price=records_head[i]['unitTP']
           head_qty=records_head[i]['inv_qty']
           head_Bonusqty=records_head[i]['inv_bonus_qty']
           head_ret_qty=records_head[i]['ret_qty']
           head_ret_bonus_qty=records_head[i]['ret_bonus_qty']

           head_invTotal=records_head[i]['actual_tp']
           head_retTotal=records_head[i]['retTP']
           reportHeadDict={'head_item':head_item,'head_unit':head_unit,'head_price':head_price,'head_qty':head_qty,'head_Bonusqty':head_Bonusqty,'head_ret_qty':head_ret_qty,'head_ret_bonus_qty':head_ret_bonus_qty,'head_invTotal':head_invTotal,'head_retTotal':head_retTotal}  
           reportHeadList.append(reportHeadDict)
           itemList.append(head_item)
           
           
        
        myString='DateRange,'+date_from+','+date_to+'\n'
        myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString+='Store,'+store_id+'|'+store_name+'\n'
        myString+='Area,'+teritory_id+'|'+teritory_name+'\n'
        myString+='Customer,'+customer_id+'|'+customer_name+'\n'
        myString+='MSO,'+mso_id+'|'+mso_name+'\n'
        myString+='Market,'+market_id+'|'+market_name+'\n\n'
                                        
       
        
        myString =myString+ '\n\nItemID , ItemName , Unit , TP ,HeadQty,HeadBonusqty,HeadinvTotal,HeadRetQty,HeadRetBonusQty,HeadRetTotal,headNetTotal,Date  ,  Inv Number   , CustomerID  ,  CustomerNmae , InvioceQnty  ,  InvioceBonus  ,  InvioceTradePrice ,ReturnQnty   , ReturnBonus  ,  ReturnTradePrice ,NetQnty  ,  NetBonus ,   NetTradePrice \n'
        p=0
        itemID=''
        invsl=''
        for i in range(len(records)):
            record=records[i]
            item_check= record['item_id']
            if itemID != record['item_id']:
                if [s for s in itemList if item_check in s]:
                    index_element = itemList.index(item_check)           
                    head_data=reportHeadList[index_element]
            netSold=record['actual_tp']-record['retTP']
            sale=record['actual_tp']
            rSale=record['retTP']
            rP=0
            if (rSale > 0):
                rP=(rSale*100)/sale
            
                  
            myString =myString+str(record['item_id'])+',' +str(record['item_name'])+','+str(head_data['head_unit'])+','+str(round(head_data['head_price']))+','+str(head_data['head_qty'])+','+str(head_data['head_Bonusqty'])+','+str(round(head_data['head_invTotal']))+','+str(head_data['head_ret_qty'])+','+str(head_data['head_ret_bonus_qty'])+','+str(round(head_data['head_retTotal']))+','+str(round(float(head_data['head_invTotal'])-float(head_data['head_retTotal'])))+','
            
            myString =myString+str(record['invoice_date'])+',INV'+str(record['depot_id'])+'-'+str(record['sl'])+','+str(record['client_id'])+',' +str(record['client_name']) +','+str(record['inv_qty'])   +','+str(record['inv_bonus_qty'])+','+ str(round(record['actual_tp'])) +',' +str(record['ret_qty'])+','+str(record['ret_bonus_qty'])+','+str(record['retTP'])+','+str(record['inv_qty']-record['ret_qty'])+','+str(record['inv_bonus_qty']-record['ret_bonus_qty'])+','+str(netSold) +'\n'
            
            itemID=record['item_id']
        
        #Save as csv
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=ProductWiseSalesStatement.csv'   
        return str(myString)



    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))       
        
        
        
# ========================================        
        
def productInvoicewiseSDwithBonus():
    c_id=session.cid   
    response.title='Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
#     if (teritory_id==''):
#         session.flash="Please select a Teritory"
#         redirect(URL(c='report_sales',f='home'))
        
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    levelRows = db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == teritory_id)).select(db.sm_level.level1,db.sm_level.level2,limitby=(0,1))
    if levelRows:
        rsm=levelRows[0].level1
        fm=levelRows[0].level2
    
    condition=''
    condition_head=''
    conditionRsm=''
    conditionFm=''
    conditionTr=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
        condition_head=condition_head+"AND depot_id = '"+str(depot_id)+"'"
        
        conditionRsm=conditionRsm+"AND depot_id = '"+str(depot_id)+"'"
        conditionFm=conditionFm+"AND depot_id = '"+str(depot_id)+"'"
        conditionTr=conditionTr+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        condition_head=condition_head+"AND store_id = '"+str(store_id)+"'"
        
        conditionRsm=conditionRsm+"AND store_id = '"+str(store_id)+"'"
        conditionFm=conditionFm+"AND store_id = '"+str(store_id)+"'"
        conditionTr=conditionTr+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
        condition_head=condition_head+"AND client_id = '"+str(customer_id)+"'"
        
        conditionRsm=conditionRsm+"AND client_id = '"+str(customer_id)+"'"
        conditionFm=conditionFm+"AND client_id = '"+str(customer_id)+"'"
        conditionTr=conditionTr+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        condition_head=condition_head+"AND rep_id = '"+str(rep_id)+"'"
        
        conditionRsm=conditionRsm+"AND rep_id = '"+str(mso_id)+"'"
        conditionFm=conditionFm+"AND rep_id = '"+str(mso_id)+"'"
        conditionTr=conditionTr+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
        condition_head=condition_head+"AND market_id = '"+str(market_id)+"'"
        
        conditionRsm=conditionRsm+"AND market_id = '"+str(market_id)+"'"
        conditionFm=conditionFm+"AND market_id = '"+str(market_id)+"'"
        conditionTr=conditionTr+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
        condition_head=condition_head+"AND area_id = '"+str(teritory_id)+"'"
        
        conditionRsm=conditionRsm+"AND area_id = '"+str(teritory_id)+"'"
        conditionFm=conditionFm+"AND area_id = '"+str(teritory_id)+"'"
        conditionTr=conditionTr+"AND area_id = '"+str(teritory_id)+"'"
        
    records_S="SELECT  depot_id,delivery_date,area_name,sl,client_id,client_name,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty > 0 AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY area_id,item_id ORDER BY area_id,item_id;"
    records=db.executesql(records_S,as_dict = True) 
    recordshead_S="SELECT  depot_id,sl,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty > 0 AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY area_id,item_id ORDER BY area_id,item_id;"

    records_head=db.executesql(recordshead_S,as_dict = True) 
    
    
    records_rsmS="SELECT  level1_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty > 0 AND    invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionRsm+"  GROUP BY level1_id ORDER BY level1_id;"
    records_fpS="SELECT  level2_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty > 0 AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionFm+"  GROUP BY level2_id ORDER BY level2_id;"
    records_trS="SELECT  level3_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty > 0 AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionTr+"  GROUP BY level3_id ORDER BY level3_id;"

    records_rsm=db.executesql(records_rsmS,as_dict = True)
    records_fp=db.executesql(records_fpS,as_dict = True)
    records_tr=db.executesql(records_trS,as_dict = True)
    
    
    
    
    

#     return records
    if records:
        reportHeadDict={}
        reportHeadList=[]
        itemList=[] 
        for i in range(len(records_head)):
           head_item=records_head[i]['item_id']
           head_unit=records_head[i]['item_unit']
           head_price=records_head[i]['unitTP']
           head_qty=records_head[i]['inv_qty']
           head_Bonusqty=records_head[i]['inv_bonus_qty']
           head_ret_qty=records_head[i]['ret_qty']
           head_ret_bonus_qty=records_head[i]['ret_bonus_qty']

           head_invTotal=records_head[i]['actual_tp']
           head_retTotal=records_head[i]['retTP']
           reportHeadDict={'head_item':head_item,'head_unit':head_unit,'head_price':head_price,'head_qty':head_qty,'head_Bonusqty':head_Bonusqty,'head_ret_qty':head_ret_qty,'head_ret_bonus_qty':head_ret_bonus_qty,'head_invTotal':head_invTotal,'head_retTotal':head_retTotal}  
           reportHeadList.append(reportHeadDict)
           itemList.append(head_item)
        return dict(records=records,reportHeadList=reportHeadList,records_rsm=records_rsm,records_fp=records_fp,records_tr=records_tr,itemList=itemList,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  teritory_id=teritory_id, teritory_name=teritory_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,page=page,items_per_page=items_per_page)
    
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))

def productInvoicewiseSDwithBonusD():
    c_id=session.cid   
    response.title='Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
#     if (teritory_id==''):
#         session.flash="Please select a Teritory"
#         redirect(URL(c='report_sales',f='home'))
        
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    levelRows = db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == teritory_id)).select(db.sm_level.level1,db.sm_level.level2,limitby=(0,1))
    if levelRows:
        rsm=levelRows[0].level1
        fm=levelRows[0].level2
    
    condition=''
    condition_head=''
    conditionRsm=''
    conditionFm=''
    conditionTr=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
        condition_head=condition_head+"AND depot_id = '"+str(depot_id)+"'"
        
        conditionRsm=conditionRsm+"AND depot_id = '"+str(depot_id)+"'"
        conditionFm=conditionFm+"AND depot_id = '"+str(depot_id)+"'"
        conditionTr=conditionTr+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        condition_head=condition_head+"AND store_id = '"+str(store_id)+"'"
        
        conditionRsm=conditionRsm+"AND store_id = '"+str(store_id)+"'"
        conditionFm=conditionFm+"AND store_id = '"+str(store_id)+"'"
        conditionTr=conditionTr+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
        condition_head=condition_head+"AND client_id = '"+str(customer_id)+"'"
        
        conditionRsm=conditionRsm+"AND client_id = '"+str(customer_id)+"'"
        conditionFm=conditionFm+"AND client_id = '"+str(customer_id)+"'"
        conditionTr=conditionTr+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        condition_head=condition_head+"AND rep_id = '"+str(rep_id)+"'"
        
        conditionRsm=conditionRsm+"AND rep_id = '"+str(mso_id)+"'"
        conditionFm=conditionFm+"AND rep_id = '"+str(mso_id)+"'"
        conditionTr=conditionTr+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
        condition_head=condition_head+"AND market_id = '"+str(market_id)+"'"
        
        conditionRsm=conditionRsm+"AND market_id = '"+str(market_id)+"'"
        conditionFm=conditionFm+"AND market_id = '"+str(market_id)+"'"
        conditionTr=conditionTr+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
        condition_head=condition_head+"AND area_id = '"+str(teritory_id)+"'"
        
        conditionRsm=conditionRsm+"AND area_id = '"+str(teritory_id)+"'"
        conditionFm=conditionFm+"AND area_id = '"+str(teritory_id)+"'"
        conditionTr=conditionTr+"AND area_id = '"+str(teritory_id)+"'"
        
    records_S="SELECT  depot_id,invoice_date,area_name,sl,client_id,client_name,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty > 0 AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY area_id,item_id ORDER BY area_id,item_id;"
    records=db.executesql(records_S,as_dict = True) 
    recordshead_S="SELECT  depot_id,sl,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty > 0 AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY area_id,item_id ORDER BY area_id,item_id;"

    records_head=db.executesql(recordshead_S,as_dict = True) 
    
    
    records_rsmS="SELECT  level1_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty > 0 AND    invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionRsm+"  GROUP BY level1_id ORDER BY level1_id;"
    records_fpS="SELECT  level2_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty > 0 AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionFm+"  GROUP BY level2_id ORDER BY level2_id;"
    records_trS="SELECT  level3_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty > 0 AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionTr+"  GROUP BY level3_id ORDER BY level3_id;"

    records_rsm=db.executesql(records_rsmS,as_dict = True)
    records_fp=db.executesql(records_fpS,as_dict = True)
    records_tr=db.executesql(records_trS,as_dict = True)
    

    if records:
        reportHeadDict={}
        reportHeadList=[]
        itemList=[] 
        for i in range(len(records_head)):
           head_item=records_head[i]['item_id']
           head_unit=records_head[i]['item_unit']
           head_price=records_head[i]['unitTP']
           head_qty=records_head[i]['inv_qty']
           head_Bonusqty=records_head[i]['inv_bonus_qty']
           head_ret_qty=records_head[i]['ret_qty']
           head_ret_bonus_qty=records_head[i]['ret_bonus_qty']

           head_invTotal=records_head[i]['actual_tp']
           head_retTotal=records_head[i]['retTP']
           reportHeadDict={'head_item':head_item,'head_unit':head_unit,'head_price':head_price,'head_qty':head_qty,'head_Bonusqty':head_Bonusqty,'head_ret_qty':head_ret_qty,'head_ret_bonus_qty':head_ret_bonus_qty,'head_invTotal':head_invTotal,'head_retTotal':head_retTotal}  
           reportHeadList.append(reportHeadDict)
           itemList.append(head_item)
           
           
        
        myString='DateRange,'+date_from+','+date_to+'\n'
        myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString+='Store,'+store_id+'|'+store_name+'\n'
        myString+='Area,'+teritory_id+'|'+teritory_name+'\n'
        myString+='Customer,'+customer_id+'|'+customer_name+'\n'
        myString+='MSO,'+mso_id+'|'+mso_name+'\n'
        myString+='Market,'+market_id+'|'+market_name+'\n\n'
                                        
       
        
        myString =myString+ '\n\nItemID , ItemName , Unit , TP ,HeadQty,HeadBonusqty,HeadinvTotal,HeadRetQty,HeadRetBonusQty,HeadRetTotal,headNetTotal,Date  ,  Inv Number   , CustomerID  ,  CustomerNmae , InvioceQnty  ,  InvioceBonus  ,  InvioceTradePrice ,ReturnQnty   , ReturnBonus  ,  ReturnTradePrice ,NetQnty  ,  NetBonus ,   NetTradePrice \n'
        p=0
        itemID=''
        invsl=''
        for i in range(len(records)):
            record=records[i]
            item_check= record['item_id']
            if itemID != record['item_id']:
                if [s for s in itemList if item_check in s]:
                    index_element = itemList.index(item_check)           
                    head_data=reportHeadList[index_element]
            netSold=record['actual_tp']-record['retTP']
            sale=record['actual_tp']
            rSale=record['retTP']
            rP=0
            if (rSale > 0):
                rP=(rSale*100)/sale
            
                  
            myString =myString+str(record['item_id'])+',' +str(record['item_name'])+','+str(head_data['head_unit'])+','+str(round(head_data['head_price']))+','+str(head_data['head_qty'])+','+str(head_data['head_Bonusqty'])+','+str(round(head_data['head_invTotal']))+','+str(head_data['head_ret_qty'])+','+str(head_data['head_ret_bonus_qty'])+','+str(round(head_data['head_retTotal']))+','+str(round(float(head_data['head_invTotal'])-float(head_data['head_retTotal'])))+','
            
            myString =myString+str(record['invoice_date'])+',INV'+str(record['depot_id'])+'-'+str(record['sl'])+','+str(record['client_id'])+',' +str(record['client_name']) +','+str(record['inv_qty'])   +','+str(record['inv_bonus_qty'])+','+ str(round(record['actual_tp'])) +',' +str(record['ret_qty'])+','+str(record['ret_bonus_qty'])+','+str(record['retTP'])+','+str(record['inv_qty']-record['ret_qty'])+','+str(record['inv_bonus_qty']-record['ret_bonus_qty'])+','+str(netSold) +'\n'
            
            itemID=record['item_id']
        
        #Save as csv
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=ProductWiseSalesStatementwithBonus.csv'   
        return str(myString)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))

# ================================        
def productInvoicewiseSDwithoutBonus():
    c_id=session.cid   
    response.title='Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
#     if (teritory_id==''):
#         session.flash="Please select a Teritory"
#         redirect(URL(c='report_sales',f='home'))
        
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    levelRows = db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == teritory_id)).select(db.sm_level.level1,db.sm_level.level2,limitby=(0,1))
    if levelRows:
        rsm=levelRows[0].level1
        fm=levelRows[0].level2
    condition=''
    condition_head=''
    conditionRsm=''
    conditionFm=''
    conditionTr=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
        condition_head=condition_head+"AND depot_id = '"+str(depot_id)+"'"
        
        conditionRsm=conditionRsm+"AND depot_id = '"+str(depot_id)+"'"
        conditionFm=conditionFm+"AND depot_id = '"+str(depot_id)+"'"
        conditionTr=conditionTr+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        condition_head=condition_head+"AND store_id = '"+str(store_id)+"'"
        
        conditionRsm=conditionRsm+"AND store_id = '"+str(store_id)+"'"
        conditionFm=conditionFm+"AND store_id = '"+str(store_id)+"'"
        conditionTr=conditionTr+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
        condition_head=condition_head+"AND client_id = '"+str(customer_id)+"'"
        
        conditionRsm=conditionRsm+"AND client_id = '"+str(customer_id)+"'"
        conditionFm=conditionFm+"AND client_id = '"+str(customer_id)+"'"
        conditionTr=conditionTr+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        condition_head=condition_head+"AND rep_id = '"+str(rep_id)+"'"
        
        conditionRsm=conditionRsm+"AND rep_id = '"+str(mso_id)+"'"
        conditionFm=conditionFm+"AND rep_id = '"+str(mso_id)+"'"
        conditionTr=conditionTr+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
        condition_head=condition_head+"AND market_id = '"+str(market_id)+"'"
        
        conditionRsm=conditionRsm+"AND market_id = '"+str(market_id)+"'"
        conditionFm=conditionFm+"AND market_id = '"+str(market_id)+"'"
        conditionTr=conditionTr+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
        condition_head=condition_head+"AND area_id = '"+str(teritory_id)+"'"
        
        conditionRsm=conditionRsm+"AND area_id = '"+str(teritory_id)+"'"
        conditionFm=conditionFm+"AND area_id = '"+str(teritory_id)+"'"
        conditionTr=conditionTr+"AND area_id = '"+str(teritory_id)+"'"
        
    records_S="SELECT  depot_id,delivery_date,area_name,sl,client_id,client_name,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty = 0 AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY area_id,item_id ORDER BY area_id,item_id;"
    records=db.executesql(records_S,as_dict = True) 
    recordshead_S="SELECT  depot_id,sl,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty = 0 AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY area_id,item_id ORDER BY area_id,item_id;"

    records_head=db.executesql(recordshead_S,as_dict = True) 
    
    
    records_rsmS="SELECT  level1_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty = 0 AND    invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionRsm+"  GROUP BY level1_id ORDER BY level1_id;"
    records_fpS="SELECT  level2_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty = 0 AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionFm+"  GROUP BY level2_id ORDER BY level2_id;"
    records_trS="SELECT  level3_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty = 0 AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionTr+"  GROUP BY level3_id ORDER BY level3_id;"

    records_rsm=db.executesql(records_rsmS,as_dict = True)
    records_fp=db.executesql(records_fpS,as_dict = True)
    records_tr=db.executesql(records_trS,as_dict = True)
    
#     return records
    if records:
        reportHeadDict={}
        reportHeadList=[]
        itemList=[] 
        for i in range(len(records_head)):
           head_item=records_head[i]['item_id']
           head_unit=records_head[i]['item_unit']
           head_price=records_head[i]['unitTP']
           head_qty=records_head[i]['inv_qty']
           head_Bonusqty=records_head[i]['inv_bonus_qty']
           head_ret_qty=records_head[i]['ret_qty']
           head_ret_bonus_qty=records_head[i]['ret_bonus_qty']

           head_invTotal=records_head[i]['actual_tp']
           head_retTotal=records_head[i]['retTP']
           reportHeadDict={'head_item':head_item,'head_unit':head_unit,'head_price':head_price,'head_qty':head_qty,'head_Bonusqty':head_Bonusqty,'head_ret_qty':head_ret_qty,'head_ret_bonus_qty':head_ret_bonus_qty,'head_invTotal':head_invTotal,'head_retTotal':head_retTotal}  
           reportHeadList.append(reportHeadDict)
           itemList.append(head_item)
        return dict(records=records,reportHeadList=reportHeadList,records_rsm=records_rsm,records_fp=records_fp,records_tr=records_tr,itemList=itemList,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  teritory_id=teritory_id, teritory_name=teritory_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,page=page,items_per_page=items_per_page)
    
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))


def productInvoicewiseSDwithoutBonusD():
    c_id=session.cid   
    response.title='Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
#     if (teritory_id==''):
#         session.flash="Please select a Teritory"
#         redirect(URL(c='report_sales',f='home'))
        
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    levelRows = db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == teritory_id)).select(db.sm_level.level1,db.sm_level.level2,limitby=(0,1))
    if levelRows:
        rsm=levelRows[0].level1
        fm=levelRows[0].level2
    
    condition=''
    condition_head=''
    conditionRsm=''
    conditionFm=''
    conditionTr=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
        condition_head=condition_head+"AND depot_id = '"+str(depot_id)+"'"
        
        conditionRsm=conditionRsm+"AND depot_id = '"+str(depot_id)+"'"
        conditionFm=conditionFm+"AND depot_id = '"+str(depot_id)+"'"
        conditionTr=conditionTr+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        condition_head=condition_head+"AND store_id = '"+str(store_id)+"'"
        
        conditionRsm=conditionRsm+"AND store_id = '"+str(store_id)+"'"
        conditionFm=conditionFm+"AND store_id = '"+str(store_id)+"'"
        conditionTr=conditionTr+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
        condition_head=condition_head+"AND client_id = '"+str(customer_id)+"'"
        
        conditionRsm=conditionRsm+"AND client_id = '"+str(customer_id)+"'"
        conditionFm=conditionFm+"AND client_id = '"+str(customer_id)+"'"
        conditionTr=conditionTr+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        condition_head=condition_head+"AND rep_id = '"+str(rep_id)+"'"
        
        conditionRsm=conditionRsm+"AND rep_id = '"+str(mso_id)+"'"
        conditionFm=conditionFm+"AND rep_id = '"+str(mso_id)+"'"
        conditionTr=conditionTr+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
        condition_head=condition_head+"AND market_id = '"+str(market_id)+"'"
        
        conditionRsm=conditionRsm+"AND market_id = '"+str(market_id)+"'"
        conditionFm=conditionFm+"AND market_id = '"+str(market_id)+"'"
        conditionTr=conditionTr+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
        condition_head=condition_head+"AND area_id = '"+str(teritory_id)+"'"
        
        conditionRsm=conditionRsm+"AND area_id = '"+str(teritory_id)+"'"
        conditionFm=conditionFm+"AND area_id = '"+str(teritory_id)+"'"
        conditionTr=conditionTr+"AND area_id = '"+str(teritory_id)+"'"
        
    records_S="SELECT  depot_id,invoice_date,area_name,sl,client_id,client_name,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty = 0 AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY area_id,item_id ORDER BY area_id,item_id;"
    records=db.executesql(records_S,as_dict = True) 
    recordshead_S="SELECT  depot_id,sl,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty = 0 AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY area_id,item_id ORDER BY area_id,item_id;"

    records_head=db.executesql(recordshead_S,as_dict = True) 
    
    
    records_rsmS="SELECT  level1_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty = 0 AND    invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionRsm+"  GROUP BY level1_id ORDER BY level1_id;"
    records_fpS="SELECT  level2_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty = 0 AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionFm+"  GROUP BY level2_id ORDER BY level2_id;"
    records_trS="SELECT  level3_id,item_id,item_name,item_unit,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty = 0 AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+conditionTr+"  GROUP BY level3_id ORDER BY level3_id;"

    records_rsm=db.executesql(records_rsmS,as_dict = True)
    records_fp=db.executesql(records_fpS,as_dict = True)
    records_tr=db.executesql(records_trS,as_dict = True)
    

    if records:
        reportHeadDict={}
        reportHeadList=[]
        itemList=[] 
        for i in range(len(records_head)):
           head_item=records_head[i]['item_id']
           head_unit=records_head[i]['item_unit']
           head_price=records_head[i]['unitTP']
           head_qty=records_head[i]['inv_qty']
           head_Bonusqty=records_head[i]['inv_bonus_qty']
           head_ret_qty=records_head[i]['ret_qty']
           head_ret_bonus_qty=records_head[i]['ret_bonus_qty']

           head_invTotal=records_head[i]['actual_tp']
           head_retTotal=records_head[i]['retTP']
           reportHeadDict={'head_item':head_item,'head_unit':head_unit,'head_price':head_price,'head_qty':head_qty,'head_Bonusqty':head_Bonusqty,'head_ret_qty':head_ret_qty,'head_ret_bonus_qty':head_ret_bonus_qty,'head_invTotal':head_invTotal,'head_retTotal':head_retTotal}  
           reportHeadList.append(reportHeadDict)
           itemList.append(head_item)
           
           
        
        myString='DateRange,'+date_from+','+date_to+'\n'
        myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString+='Store,'+store_id+'|'+store_name+'\n'
        myString+='Area,'+teritory_id+'|'+teritory_name+'\n'
        myString+='Customer,'+customer_id+'|'+customer_name+'\n'
        myString+='MSO,'+mso_id+'|'+mso_name+'\n'
        myString+='Market,'+market_id+'|'+market_name+'\n\n'
                                        
       
        
        myString =myString+ '\n\nItemID , ItemName , Unit , TP ,HeadQty,HeadBonusqty,HeadinvTotal,HeadRetQty,HeadRetBonusQty,HeadRetTotal,headNetTotal,Date  ,  Inv Number   , CustomerID  ,  CustomerNmae , InvioceQnty  ,  InvioceBonus  ,  InvioceTradePrice ,ReturnQnty   , ReturnBonus  ,  ReturnTradePrice ,NetQnty  ,  NetBonus ,   NetTradePrice \n'
        p=0
        itemID=''
        invsl=''
        for i in range(len(records)):
            record=records[i]
            item_check= record['item_id']
            if itemID != record['item_id']:
                if [s for s in itemList if item_check in s]:
                    index_element = itemList.index(item_check)           
                    head_data=reportHeadList[index_element]
            netSold=record['actual_tp']-record['retTP']
            sale=record['actual_tp']
            rSale=record['retTP']
            rP=0
            if (rSale > 0):
                rP=(rSale*100)/sale
            
                  
            myString =myString+str(record['item_id'])+',' +str(record['item_name'])+','+str(head_data['head_unit'])+','+str(round(head_data['head_price']))+','+str(head_data['head_qty'])+','+str(head_data['head_Bonusqty'])+','+str(round(head_data['head_invTotal']))+','+str(head_data['head_ret_qty'])+','+str(head_data['head_ret_bonus_qty'])+','+str(round(head_data['head_retTotal']))+','+str(round(float(head_data['head_invTotal'])-float(head_data['head_retTotal'])))+','
            
            myString =myString+str(record['invoice_date'])+',INV'+str(record['depot_id'])+'-'+str(record['sl'])+','+str(record['client_id'])+',' +str(record['client_name']) +','+str(record['inv_qty'])   +','+str(record['inv_bonus_qty'])+','+ str(round(record['actual_tp'])) +',' +str(record['ret_qty'])+','+str(record['ret_bonus_qty'])+','+str(record['retTP'])+','+str(record['inv_qty']-record['ret_qty'])+','+str(record['inv_bonus_qty']-record['ret_bonus_qty'])+','+str(netSold) +'\n'
            
            itemID=record['item_id']
        
        #Save as csv
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=ProductWiseSalesStatementwithBonus.csv'   
        return str(myString)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
        
        

        









# =====================================================


        
def invoicewiseSD():
    
    c_id=session.cid   
    response.title='Invoice Wise Sales Detail'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()

    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
#     if (teritory_id==''):
#         session.flash="Please select a Teritory"
#         redirect(URL(c='report_sales',f='home'))
        
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    levelRows = db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == teritory_id)).select(db.sm_level.level1,db.sm_level.level2,limitby=(0,1))
    if levelRows:
        rsm=levelRows[0].level1
        fm=levelRows[0].level2
    condition=''
   
    conditionRsm=''
    conditionFm=''
    conditionTr=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
       
        
        conditionRsm=conditionRsm+"AND depot_id = '"+str(depot_id)+"'"
        conditionFm=conditionFm+"AND depot_id = '"+str(depot_id)+"'"
        conditionTr=conditionTr+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        
        
        conditionRsm=conditionRsm+"AND store_id = '"+str(store_id)+"'"
        conditionFm=conditionFm+"AND store_id = '"+str(store_id)+"'"
        conditionTr=conditionTr+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
       
        
        conditionRsm=conditionRsm+"AND client_id = '"+str(customer_id)+"'"
        conditionFm=conditionFm+"AND client_id = '"+str(customer_id)+"'"
        conditionTr=conditionTr+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        
        
        conditionRsm=conditionRsm+"AND rep_id = '"+str(mso_id)+"'"
        conditionFm=conditionFm+"AND rep_id = '"+str(mso_id)+"'"
        conditionTr=conditionTr+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
        
        
        conditionRsm=conditionRsm+"AND market_id = '"+str(market_id)+"'"
        conditionFm=conditionFm+"AND market_id = '"+str(market_id)+"'"
        conditionTr=conditionTr+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
        
        
        conditionRsm=conditionRsm+"AND area_id = '"+str(teritory_id)+"'"
        conditionFm=conditionFm+"AND area_id = '"+str(teritory_id)+"'"
        conditionTr=conditionTr+"AND area_id = '"+str(teritory_id)+"'"
        
    records_S="SELECT  depot_id,sl,invoice_date,client_id,client_name,rep_id,rep_name,market_name,market_id,sum(actual_total_tp) as actual_tp, sum(return_tp+return_sp_discount) as retTP ,sum(vat_total_amount-return_vat) as vat ,sum(discount-return_discount) as discount ,sum(sp_discount-return_sp_discount) as spDiscount FROM sm_invoice_head WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY sl ORDER BY sl;"
#     return records_S
    records=db.executesql(records_S,as_dict = True) 
    
    
    

    if records:
        return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  teritory_id=teritory_id, teritory_name=teritory_name,  mso_id=mso_id, mso_name=mso_name,page=page,items_per_page=items_per_page)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))

# ===============Download===================
def invoicewiseSDLoad():
    
    c_id=session.cid   
    response.title='Invoice Wise Sales Detail'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()

    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
#     if (teritory_id==''):
#         session.flash="Please select a Teritory"
#         redirect(URL(c='report_sales',f='home'))
        
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    levelRows = db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == teritory_id)).select(db.sm_level.level1,db.sm_level.level2,limitby=(0,1))
    if levelRows:
        rsm=levelRows[0].level1
        fm=levelRows[0].level2
    condition=''
   
    conditionRsm=''
    conditionFm=''
    conditionTr=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
       
        
        conditionRsm=conditionRsm+"AND depot_id = '"+str(depot_id)+"'"
        conditionFm=conditionFm+"AND depot_id = '"+str(depot_id)+"'"
        conditionTr=conditionTr+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        
        
        conditionRsm=conditionRsm+"AND store_id = '"+str(store_id)+"'"
        conditionFm=conditionFm+"AND store_id = '"+str(store_id)+"'"
        conditionTr=conditionTr+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
       
        
        conditionRsm=conditionRsm+"AND client_id = '"+str(customer_id)+"'"
        conditionFm=conditionFm+"AND client_id = '"+str(customer_id)+"'"
        conditionTr=conditionTr+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        
        
        conditionRsm=conditionRsm+"AND rep_id = '"+str(mso_id)+"'"
        conditionFm=conditionFm+"AND rep_id = '"+str(mso_id)+"'"
        conditionTr=conditionTr+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
        
        
        conditionRsm=conditionRsm+"AND market_id = '"+str(market_id)+"'"
        conditionFm=conditionFm+"AND market_id = '"+str(market_id)+"'"
        conditionTr=conditionTr+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
        
        
        conditionRsm=conditionRsm+"AND area_id = '"+str(teritory_id)+"'"
        conditionFm=conditionFm+"AND area_id = '"+str(teritory_id)+"'"
        conditionTr=conditionTr+"AND area_id = '"+str(teritory_id)+"'"
        
    records_S="SELECT  depot_id,sl,invoice_date,client_id,client_name,rep_id,rep_name,market_name,market_id,sum(actual_total_tp) as actual_tp, sum(return_tp+return_sp_discount) as retTP ,sum(vat_total_amount-return_vat) as vat ,sum(discount-return_discount) as discount ,sum(sp_discount-return_sp_discount) as spDiscount FROM sm_invoice_head WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY sl ORDER BY sl;"
#     return records_S
    records=db.executesql(records_S,as_dict = True) 
    
    if records:
        myString='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString+='Store,'+store_id+'|'+store_name+'\n'
        myString+='Customer,'+customer_id+'|'+customer_name+'\n'
        myString+='Area,'+teritory_id+'|'+teritory_name+'\n'
        myString+='MSO,'+mso_id+'|'+mso_name+'\n\n'
        myString=myString+'Date  ,  Inv Number ,   CustomerID,CustomerName ,   MSOID,MsoName  ,  MaketID,MarketName  ,  InvioceTradePrice,    ReturnTradePrice,    NetTP,NetDisc ,NetSpDisc  ,  NetVat ,   NetTradePrice\n'
    
        for i in range(len(records)):
            record=records[i]
            delivery_date =record['invoice_date'].strftime('%d-%b-%Y')
            InvNumber='INV'+str(record['depot_id'])+'-'+str(record['sl'])
            CustomerID =record['client_id']
            CustomerName=record['client_name']
            MSOID=record['rep_id']
            MsoName=record['rep_name']
            MaketID=record['market_id']
            MarketName=record['market_name']
            sale=(record['actual_tp']+record['vat'])-record['discount']-record['spDiscount']
            rSale=record['retTP']
            netSold=(record['actual_tp']-rSale)+record['vat']-record['discount']-record['spDiscount']

            InvioceTradePrice=record['actual_tp']
            ReturnTradePrice=record['retTP']
            NetTP=record['actual_tp']-record['retTP']
            NetDisc =record['discount']
            NetspDiscount=record['spDiscount']
            NetVat    =record['vat']
            NetTradePrice=netSold
    
                                                                                                                                                        
            
            myString=myString+str(delivery_date)+','+str(InvNumber)+','+str(CustomerID)+','+str(CustomerName)+','+str(MSOID)+','+str(MsoName)+','+str(MaketID)+','+str(MarketName)+','+str(round(sale,2))+','+str(round(InvioceTradePrice,2))+','+str(round(ReturnTradePrice,2))+','+str(round(NetTP,2))+','+str(round(NetDisc,2))+','+str(round(NetVat,2))+','+str(round(NetTradePrice,2))+'\n'
            
    
    
        #Save as csv
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=InvoiceWiseSalesDetail.csv'   
        return str(myString)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))



def causeofRet():  
    c_id=session.cid   
    response.title='Product Wise Sales Statement'       
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()

    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  
    
    qset=db()
    qset=qset(db.sm_return_head.cid==c_id)
    qset=qset(db.sm_return_head.status=='Returned')
    qset=qset((db.sm_return_head.return_date >= date_from) & (db.sm_return_head.return_date < date_to_m))

    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.return_tp > 0)  
    qset=qset(db.sm_invoice_head.status=='Invoiced')    
    qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    qset=qset(db.sm_invoice_head.sl == db.sm_return_head.invoice_sl  )  


    
    qset_inv=db()

    qset_inv=qset_inv(db.sm_invoice_head.cid==c_id)
    qset_inv=qset_inv(db.sm_invoice_head.return_tp > 0)  
    
    qset_inv=qset_inv(db.sm_invoice_head.status=='Invoiced')    
    qset_inv=qset_inv((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    if (depot_id!=''):
        qset=qset(db.sm_return_head.depot_id==depot_id)
        qset_inv=qset_inv(db.sm_invoice_head.depot_id==depot_id)
        
    if (store_id!=''):
        qset=qset(db.sm_return_head.store_id==store_id)   
        qset_inv=qset_inv(db.sm_invoice_head.store_id==store_id)
        
    if (customer_id!=''):
        qset=qset(db.sm_return_head.client_id==customer_id)
        qset_inv=qset_inv(db.sm_invoice_head.client_id==client_id)
    if (teritory_id!=''):
        qset=qset(db.sm_return_head.area_id==teritory_id)
        qset_inv=qset_inv(db.sm_invoice_head.area_id==teritory_id)
    if (mso_id!=''):
        qset=qset(db.sm_return_head.rep_id==mso_id) 
        qset_inv=qset_inv(db.sm_invoice_head.rep_id==rep_id)
        
    records=qset.select(db.sm_invoice_head.d_man_id,db.sm_return_head.return_date,db.sm_return_head.ret_reason,db.sm_return_head.total_amount.sum(),db.sm_return_head.id.count(), orderby=db.sm_invoice_head.d_man_id | db.sm_return_head.return_date|db.sm_return_head.ret_reason,groupby=db.sm_invoice_head.d_man_id | db.sm_return_head.return_date|db.sm_return_head.ret_reason)
#     return db._lastsql
    ret_str=''
    retDeate_past=''
    dman_past=''
    for records in records:      
        retDman = records[db.sm_invoice_head.d_man_id]
        retDeate = records[db.sm_return_head.return_date]
        ret_reason= records[db.sm_return_head.ret_reason]
        ret_count= records[db.sm_return_head.id.count()]
        ret_amn= records[db.sm_return_head.total_amount.sum()]
        if retDeate_past=='':
            ret_str =str(retDman)+'|'+str(retDeate)+'fdfd'+str(ret_reason)+'fdfd'+str(ret_count)+'fdfd'+str(ret_amn)
        else:
            if retDeate_past != str(retDeate):
                ret_str =ret_str+'fdfd'+str(retDman)+'|'+str(retDeate)+'fdfd'+str(ret_reason)+'fdfd'+str(ret_count)+'fdfd'+str(ret_amn)
            else:
                ret_str=ret_str+'fdfd'+str(retDman)+'|'+str(ret_reason)+'fdfd'+str(ret_count)+'fdfd'+str(ret_amn)
        
        
        retDeate_past=str(retDeate)
        
        
#     return ret_str    
    records_inv=qset_inv.select(db.sm_invoice_head.ALL,db.sm_invoice_head.id.count(),db.sm_invoice_head.total_amount.sum(),((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_discount+db.sm_invoice_head.return_sp_discount)-db.sm_invoice_head.return_discount+db.sm_invoice_head.return_vat).sum(), orderby=db.sm_invoice_head.d_man_id | db.sm_invoice_head.invoice_date,groupby=db.sm_invoice_head.d_man_id | db.sm_invoice_head.invoice_date)


    return dict(records_inv=records_inv,ret_str=ret_str,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  teritory_id=teritory_id, teritory_name=teritory_name,  mso_id=mso_id, mso_name=mso_name)
    
           
def causeofRetD():  
    c_id=session.cid   
    response.title='Product Wise Sales Statement'       
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()

    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  
    
    qset=db()
    qset=qset(db.sm_return_head.cid==c_id)
    qset=qset(db.sm_return_head.status=='Returned')
    qset=qset((db.sm_return_head.return_date >= date_from) & (db.sm_return_head.return_date < date_to_m))

    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.return_tp > 0)  
    qset=qset(db.sm_invoice_head.status=='Invoiced')    
    qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    qset=qset(db.sm_invoice_head.sl == db.sm_return_head.invoice_sl  )  


    
    qset_inv=db()

    qset_inv=qset_inv(db.sm_invoice_head.cid==c_id)
    qset_inv=qset_inv(db.sm_invoice_head.return_tp > 0)  
    
    qset_inv=qset_inv(db.sm_invoice_head.status=='Invoiced')    
    qset_inv=qset_inv((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    if (depot_id!=''):
        qset=qset(db.sm_return_head.depot_id==depot_id)
        qset_inv=qset_inv(db.sm_invoice_head.depot_id==depot_id)
        
    if (store_id!=''):
        qset=qset(db.sm_return_head.store_id==store_id)   
        qset_inv=qset_inv(db.sm_invoice_head.store_id==store_id)
        
    if (customer_id!=''):
        qset=qset(db.sm_return_head.client_id==customer_id)
        qset_inv=qset_inv(db.sm_invoice_head.client_id==client_id)
    if (teritory_id!=''):
        qset=qset(db.sm_return_head.area_id==teritory_id)
        qset_inv=qset_inv(db.sm_invoice_head.area_id==teritory_id)
    if (mso_id!=''):
        qset=qset(db.sm_return_head.rep_id==mso_id) 
        qset_inv=qset_inv(db.sm_invoice_head.rep_id==rep_id)
        
    records=qset.select(db.sm_invoice_head.d_man_id,db.sm_return_head.return_date,db.sm_return_head.ret_reason,db.sm_return_head.total_amount.sum(),db.sm_return_head.id.count(), orderby=db.sm_invoice_head.d_man_id | db.sm_return_head.return_date|db.sm_return_head.ret_reason,groupby=db.sm_invoice_head.d_man_id | db.sm_return_head.return_date|db.sm_return_head.ret_reason)
#     return db._lastsql
    ret_str=''
    retDeate_past=''
    dman_past=''
    for records in records:      
        retDman = records[db.sm_invoice_head.d_man_id]
        retDeate = records[db.sm_return_head.return_date]
        ret_reason= records[db.sm_return_head.ret_reason]
        ret_count= records[db.sm_return_head.id.count()]
        ret_amn= records[db.sm_return_head.total_amount.sum()]
        if retDeate_past=='':
            ret_str =str(retDman)+'|'+str(retDeate)+'fdfd'+str(ret_reason)+'fdfd'+str(ret_count)+'fdfd'+str(ret_amn)
        else:
            if retDeate_past != str(retDeate):
                ret_str =ret_str+'fdfd'+str(retDman)+'|'+str(retDeate)+'fdfd'+str(ret_reason)+'fdfd'+str(ret_count)+'fdfd'+str(ret_amn)
            else:
                ret_str=ret_str+'fdfd'+str(retDman)+'|'+str(ret_reason)+'fdfd'+str(ret_count)+'fdfd'+str(ret_amn)
        
        
        retDeate_past=str(retDeate)
        
        
#     return ret_str    
    records_inv=qset_inv.select(db.sm_invoice_head.ALL,db.sm_invoice_head.id.count(),db.sm_invoice_head.total_amount.sum(),((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_discount+db.sm_invoice_head.return_sp_discount)-db.sm_invoice_head.return_discount+db.sm_invoice_head.return_vat).sum(), orderby=db.sm_invoice_head.d_man_id | db.sm_invoice_head.invoice_date,groupby=db.sm_invoice_head.d_man_id | db.sm_invoice_head.invoice_date)


    
    
    
    myString='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='Store,'+store_id+'|'+store_name+'\n'
    myString+='Customer,'+customer_id+'|'+customer_name+'\n'
    myString+='MSO,'+mso_id+'|'+mso_name+'\n\n'
    
    
        
    myString+='InvoiceDate , Doc/Tp, Invoice, Rerurn ,NextDay Delivery ,Cancelled CashShort , Shop Closed  ,  Product Short  ,  Not Delivered  ,  Not Ordered   , Computer Mistake  ,  Part Sale  ,  Not Mentioned\n'
    
    dp_past=''
    for record in records_inv:
        srt_get=''
        ret_reason= ''
        ret_count_sclosed= 0
        ret_amn_sclosed=0.0
        ret_count_cacShop= 0
        ret_amn_cacShop=0.0
        ret_count_ndd= 0
        ret_amn_ndd=0.0
        ret_count_pShort= 0
        ret_amn_pShort=0.0
        ret_count_nd= 0
        ret_amn_nd=0.0
        ret_count_no= 0
        ret_amn_no=0.0
        ret_count_cm= 0
        ret_amn_cm=0.0
        ret_count_psale= 0
        ret_amn_psale=0.0
        ret_count_nm= 0
        ret_amn_nm=0.0
        
        invoice_date =str(record[db.sm_invoice_head.invoice_date])
        splitstr=str(record[db.sm_invoice_head.d_man_id])+'|'+invoice_date
        
        if ret_str.find(splitstr)!=-1:
                srt_get= invoice_date+ret_str.split(splitstr)[1]

        reason='CANCELLED AND CASH SHORT'
        if (srt_get.find(reason)!=-1):
            reasonStr=srt_get.split(reason)[1]
            ret_count_cacShop= int(reasonStr.split('fdfd')[1])
            ret_amn_cacShop= float(reasonStr.split('fdfd')[2])
            
        reason='SHOP CLOSED'
        if (srt_get.find(reason)!=-1):
            reasonStr=srt_get.split(reason)[1]
            ret_count_sclosed= int(reasonStr.split('fdfd')[1])
            ret_amn_sclosed= float(reasonStr.split('fdfd')[2])

        reason='NEX DAY DELIVERY'
        if (srt_get.find(reason)!=-1):
            reasonStr=srt_get.split(reason)[1]
            ret_count_ndd= int(reasonStr.split('fdfd')[1])
            ret_amn_ndd= float(reasonStr.split('fdfd')[2])

        reason='PRODUCT SHORT'
        if (srt_get.find(reason)!=-1):
            reasonStr=srt_get.split(reason)[1]
            ret_count_pShort= int(reasonStr.split('fdfd')[1])
            ret_amn_pShort= float(reasonStr.split('fdfd')[2])

        reason='NOT DELIVERED'
        if (srt_get.find(reason)!=-1):
            reasonStr=srt_get.split(reason)[1]
            ret_count_nd= int(reasonStr.split('fdfd')[1])
            ret_amn_nd= float(reasonStr.split('fdfd')[2])

        reason='NOT ORDERED'
        if (srt_get.find(reason)!=-1):
            reasonStr=srt_get.split(reason)[1]
            ret_count_no= int(reasonStr.split('fdfd')[1])
            ret_amn_no= float(reasonStr.split('fdfd')[2])
              
        reason='COMPUTER MISTAKE'
        if (srt_get.find(reason)!=-1):
            reasonStr=srt_get.split(reason)[1]
            ret_count_cm= int(reasonStr.split('fdfd')[1])
            ret_amn_cm= float(reasonStr.split('fdfd')[2])
                
        reason='PART SALE'
        if (srt_get.find(reason)!=-1):
            reasonStr=srt_get.split(reason)[1]
            ret_count_psale= int(reasonStr.split('fdfd')[1])
            ret_amn_psale= float(reasonStr.split('fdfd')[2])

        reason='NOT MENTIONED'
        if (srt_get.find(reason)!=-1):
            reasonStr=srt_get.split(reason)[1]
            ret_count_nm= int(reasonStr.split('fdfd')[1])
            ret_amn_nm= float(reasonStr.split('fdfd')[2])
        
        total_ret_count=ret_count_cacShop+ret_count_sclosed+ret_count_ndd+ret_count_pShort+ret_count_nd+ret_count_no+ret_count_cm+ret_count_psale+ret_count_nm
        total_retamn=ret_amn_cacShop+ret_amn_sclosed+ret_amn_ndd+ret_amn_pShort+ret_amn_nd+ret_amn_no+ret_amn_cm+ret_amn_psale+ret_amn_nm
#         return total_retamn
        
        if ( dp_past!=record[db.sm_invoice_head.d_man_id]):
              myString=myString+'Delivery Person: '+str(record[db.sm_invoice_head.d_man_id])+'-'+str(record[db.sm_invoice_head.d_man_name])+'\n'
                                                                                                                                                                       
        myString=myString+str(record[db.sm_invoice_head.invoice_date])+','+'Document'+','+str(record[db.sm_invoice_head.id.count()])+','+str(total_ret_count)+','+str(ret_count_ndd)+','+str(ret_count_cacShop)+','+str(ret_count_sclosed)+','+str(ret_count_pShort)+','+str(ret_count_nd)+','+str(ret_count_no)+','+str(ret_count_cm)+','+str(ret_count_psale)+','+str(ret_count_nm)+'\n'
        myString=myString+','+'TP'+','+str(record[db.sm_invoice_head.total_amount.sum()])+','+str(total_retamn)+','+str(ret_amn_ndd)+','+str(ret_count_cacShop)+','+str(ret_amn_sclosed)+','+str(ret_amn_pShort)+','+str(ret_amn_nd)+','+str(ret_amn_no)+','+str(ret_amn_cm)+','+str(ret_amn_psale)+','+str(ret_amn_nm)+'\n'
        dp_past=record[db.sm_invoice_head.d_man_id]


    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=CauseofReturn.csv'   
    return str(myString) 
    
    

            
def summaryReport():  
    c_id=session.cid   
    response.title='Summary Report'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()

    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

        
    
    qset_sum=db()
    qset_sum=qset_sum(db.sm_invoice_head.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice_head.status=='Invoiced')
    qset_sum=qset_sum((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))

    if (depot_id!=''):
        qset_sum=qset_sum(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset_sum=qset_sum(db.sm_invoice_head.store_id==store_id)   
    if (customer_id!=''):
        qset_sum=qset_sum(db.sm_invoice_head.client_id==customer_id)
    if (teritory_id!=''):
        qset_sum=qset_sum(db.sm_invoice_head.area_id==teritory_id)
    if (mso_id!=''):
        qset_sum=qset_sum(db.sm_invoice_head.rep_id==mso_id) 
        
    records=qset_sum.select(db.sm_invoice_head.level1_id,db.sm_invoice_head.level2_id,db.sm_invoice_head.level3_id,   db.sm_invoice_head.level1_name,db.sm_invoice_head.level2_name,db.sm_invoice_head.level3_name ,db.sm_invoice_head.actual_total_tp.sum(),(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.id.count(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.vat_total_amount.sum(),(db.sm_invoice_head.discount).sum(),(db.sm_invoice_head.sp_discount).sum(),(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),(db.sm_invoice_head.return_discount).sum(),(db.sm_invoice_head.return_sp_discount).sum(),(db.sm_invoice_head.return_discount+db.sm_invoice_head.return_sp_discount).sum(), orderby=db.sm_invoice_head.level1_id|db.sm_invoice_head.level2_id|db.sm_invoice_head.level3_id,groupby=db.sm_invoice_head.level1_id|db.sm_invoice_head.level2_id|db.sm_invoice_head.level3_id)
#     return records
#     return db._lastsql
    
    return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  teritory_id=teritory_id, teritory_name=teritory_name,  mso_id=mso_id, mso_name=mso_name)   
def summaryReportD():  
    c_id=session.cid   
    response.title='Summary Report'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()

    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

        
    
    qset_sum=db()
    qset_sum=qset_sum(db.sm_invoice_head.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice_head.status=='Invoiced')
    qset_sum=qset_sum((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))

    if (depot_id!=''):
        qset_sum=qset_sum(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset_sum=qset_sum(db.sm_invoice_head.store_id==store_id)   
    if (customer_id!=''):
        qset_sum=qset_sum(db.sm_invoice_head.client_id==customer_id)
    if (teritory_id!=''):
        qset_sum=qset_sum(db.sm_invoice_head.area_id==teritory_id)
    if (mso_id!=''):
        qset_sum=qset_sum(db.sm_invoice_head.rep_id==mso_id) 
        
    records=qset_sum.select(db.sm_invoice_head.level1_id,db.sm_invoice_head.level2_id,db.sm_invoice_head.level3_id,   db.sm_invoice_head.level1_name,db.sm_invoice_head.level2_name,db.sm_invoice_head.level3_name ,db.sm_invoice_head.actual_total_tp.sum(),(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.id.count(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.vat_total_amount.sum(),(db.sm_invoice_head.discount).sum(),(db.sm_invoice_head.sp_discount).sum(),(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),(db.sm_invoice_head.return_discount).sum(),(db.sm_invoice_head.return_sp_discount).sum(),(db.sm_invoice_head.return_discount+db.sm_invoice_head.return_sp_discount).sum(), orderby=db.sm_invoice_head.level1_id|db.sm_invoice_head.level2_id|db.sm_invoice_head.level3_id,groupby=db.sm_invoice_head.level1_id|db.sm_invoice_head.level2_id|db.sm_invoice_head.level3_id)
    
    #REmove , from record.Cause , means new column in excel    
    myString='Daterange,'+date_from+','+date_to+'\n'
    myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    
    
   
    
   
        
    myString+='RSM ,RSMName ,  FM ,FMName ,  TR,TRName   , InvCount ,InvTotalTP, InvVat ,  InvDisc ,InvSPDisc,InvAmount,RetTotalTP ,RetVat,  RetDisc ,RetSPDisc,RetAmount, Net\n'
    
    rsm_past=''
    fm_past=''
    tr_past=''
    for records in records:
        rsm=records[db.sm_invoice_head.level1_id]
        rsm_name=records[db.sm_invoice_head.level1_name]
        fm=records[db.sm_invoice_head.level2_id]
        fm_name=records[db.sm_invoice_head.level2_name]
        tr=records[db.sm_invoice_head.level3_id]
        tr_name=records[db.sm_invoice_head.level3_name]
        invCount=records[db.sm_invoice_head.id.count()]
        invtTP=(records[db.sm_invoice_head.total_amount.sum()]+records[(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum()])-records[db.sm_invoice_head.vat_total_amount.sum()]
        invVat=records[db.sm_invoice_head.vat_total_amount.sum()]
        invSpDisc=records[db.sm_invoice_head.sp_discount.sum()]
        invRDisc=records[db.sm_invoice_head.discount.sum()]
        invDisc=records[(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum()]
        invAmn=records[db.sm_invoice_head.total_amount.sum()]
        rettTP=records[db.sm_invoice_head.return_tp.sum()]
        retVat=records[db.sm_invoice_head.return_vat.sum()]
        retDisc=records[(db.sm_invoice_head.return_discount+db.sm_invoice_head.return_sp_discount).sum()]
        retSPDisc=records[db.sm_invoice_head.return_sp_discount.sum()]
        retRDisc=records[db.sm_invoice_head.return_discount.sum()]
        retAmn=records[db.sm_invoice_head.return_tp.sum()]+records[db.sm_invoice_head.return_vat.sum()]-records[(db.sm_invoice_head.return_discount+db.sm_invoice_head.return_sp_discount).sum()]
        net=records[db.sm_invoice_head.total_amount.sum()]-retAmn
    
    

         
              
        myString+=str(rsm)+','+str(rsm_name)+','+str(fm)+','+str(fm_name)+','+str(tr)+','+str(tr_name)+','+str(invCount)+','+str(round(invtTP,2))+','+str(invVat)+','+str(invRDisc)+','+str(invSpDisc)+','+str(invAmn)+','+str(rettTP)+','+str(retVat)+','+str(retRDisc)+','+str(retSPDisc)+','+str(retAmn)+','+str(net)+'\n'
        
        
        
#         rsm_past=records[db.sm_invoice_head.level1_id]
#         fm_past=records[db.sm_invoice_head.level2_id]
#         tr_past=records[db.sm_invoice_head.level3_id]
        
       
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=SummaryReport.csv'   
    return str(myString) 
    
#     return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  teritory_id=teritory_id, teritory_name=teritory_name,  mso_id=mso_id, mso_name=mso_name)   

def dp_wise_sale_ss():
    c_id=session.cid   
#     return c_id
    response.title='Delivery Person Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    dman_id=str(request.vars.dman_id).strip()
    dman_name=str(request.vars.dman_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  
#     return dman_id
        
#     if (dman_id==""):
#         session.flash="Please select deliery person."
#         redirect(URL(c='report_sales',f='home'))
        
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    qset_fr=db()
    qset_fr=qset_fr(db.sm_invoice_head.cid==c_id)
    qset_fr=qset_fr(db.sm_invoice_head.status=='Invoiced')
    qset_fr=qset_fr((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    qset_fr=qset_fr(db.sm_invoice_head.actual_total_tp == (db.sm_invoice_head.return_tp+db.sm_invoice_head.return_sp_discount))

    if (depot_id!=''):
        qset=qset(db.sm_invoice_head.depot_id==depot_id)
        qset_fr=qset_fr(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice_head.store_id==store_id)   
        qset_fr=qset_fr(db.sm_invoice_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_invoice_head.client_id==client_id)
        qset_fr=qset_fr(db.sm_invoice_head.client_id==client_id)
    if (teritory_id!=''):
        qset=qset(db.sm_invoice_head.area_id==teritory_id)
        qset_fr=qset_fr(db.sm_invoice_head.area_id==teritory_id)
    if (mso_id!=''):
        qset=qset(db.sm_invoice_head.rep_id==mso_id) 
        qset_fr=qset_fr(db.sm_invoice_head.rep_id==mso_id) 
    if (dman_id!=''):
        qset=qset(db.sm_invoice_head.d_man_id==dman_id)
        qset_fr=qset_fr(db.sm_invoice_head.d_man_id==dman_id) 
    if (market_id!=''):
        qset=qset(db.sm_invoice_head.market_id==market_id)
        qset_fr=qset_fr(db.sm_invoice_head.market_id==market_id)

        
    records=qset.select(db.sm_invoice_head.d_man_id,db.sm_invoice_head.d_man_name,db.sm_invoice_head.id.count(),db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.vat_total_amount.sum(),(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),(db.sm_invoice_head.return_discount+db.sm_invoice_head.return_sp_discount).sum(), orderby=db.sm_invoice_head.d_man_id,groupby=db.sm_invoice_head.d_man_id)
    
    
    records_fr=qset_fr.select(db.sm_invoice_head.d_man_id,db.sm_invoice_head.id.count(), orderby=db.sm_invoice_head.d_man_id,groupby=db.sm_invoice_head.d_man_id)
#     return records_fr
#     return db._lastsql
     
    dmanList=[]
    invCList=[]
    for records_fr in records_fr:
        dman_id = records_fr[db.sm_invoice_head.d_man_id]
        invCount = records_fr[db.sm_invoice_head.id.count()]
        dmanList.append(dman_id)
        invCList.append(invCount)
    if records:
        return dict(records=records,dmanList=dmanList,invCList=invCList,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  teritory_id=teritory_id, teritory_name=teritory_name, dman_id=dman_id,dman_name=dman_name, mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name)

    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))

def dp_wise_sale_ssD():
    c_id=session.cid   
#     return c_id
    response.title='Delivery Person Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    dman_id=str(request.vars.dman_id).strip()
    dman_name=str(request.vars.dman_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  
#     return dman_id
        
#     if (dman_id==""):
#         session.flash="Please select deliery person."
#         redirect(URL(c='report_sales',f='home'))
        
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    qset_fr=db()
    qset_fr=qset_fr(db.sm_invoice_head.cid==c_id)
    qset_fr=qset_fr(db.sm_invoice_head.status=='Invoiced')
    qset_fr=qset_fr((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    qset_fr=qset_fr(db.sm_invoice_head.actual_total_tp == (db.sm_invoice_head.return_tp+db.sm_invoice_head.return_sp_discount))

    if (depot_id!=''):
        qset=qset(db.sm_invoice_head.depot_id==depot_id)
        qset_fr=qset_fr(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice_head.store_id==store_id)   
        qset_fr=qset_fr(db.sm_invoice_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_invoice_head.client_id==client_id)
        qset_fr=qset_fr(db.sm_invoice_head.client_id==client_id)
    if (teritory_id!=''):
        qset=qset(db.sm_invoice_head.area_id==teritory_id)
        qset_fr=qset_fr(db.sm_invoice_head.area_id==teritory_id)
    if (mso_id!=''):
        qset=qset(db.sm_invoice_head.rep_id==mso_id) 
        qset_fr=qset_fr(db.sm_invoice_head.rep_id==mso_id) 
    if (dman_id!=''):
        qset=qset(db.sm_invoice_head.d_man_id==dman_id)
        qset_fr=qset_fr(db.sm_invoice_head.d_man_id==dman_id) 
    if (market_id!=''):
        qset=qset(db.sm_invoice_head.market_id==market_id)
        qset_fr=qset_fr(db.sm_invoice_head.market_id==market_id)

        
    records=qset.select(db.sm_invoice_head.d_man_id,db.sm_invoice_head.d_man_name,db.sm_invoice_head.id.count(),db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.vat_total_amount.sum(),(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),(db.sm_invoice_head.return_discount+db.sm_invoice_head.return_sp_discount).sum(), orderby=db.sm_invoice_head.d_man_id,groupby=db.sm_invoice_head.d_man_id)
    
    
    records_fr=qset_fr.select(db.sm_invoice_head.d_man_id,db.sm_invoice_head.id.count(), orderby=db.sm_invoice_head.d_man_id,groupby=db.sm_invoice_head.d_man_id)
#     return records_fr
#     return db._lastsql
     
    dmanList=[]
    invCList=[]
    for records_fr in records_fr:
        dman_id = records_fr[db.sm_invoice_head.d_man_id]
        invCount = records_fr[db.sm_invoice_head.id.count()]
        dmanList.append(dman_id)
        invCList.append(invCount)
            
    
    #REmove , from record.Cause , means new column in excel    
    myString='Daterange,'+date_from+','+date_to+'\n'
    myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='Store,'+store_id+'|'+store_name+'\n'
    myString+='Teritory,'+teritory_id+'|'+teritory_name+'\n'
    myString+='DeliveryMan,'+dman_id+'|'+dman_name+'\n'
    myString+='Customer,'+customer_id+'|'+customer_name+'\n'
    myString+='MSO,'+mso_id+'|'+mso_name+'\n'
    myString+='Market,'+market_id+'|'+market_name+'\n\n'
    
   
        
    myString+='DP ID ,   Delivery Person Name ,   No of Inv.  ,  Full Return No  ,  Inv Amnt ,   Ret Amnt ,   Exec%  ,  Ret%  ,  Net Sold TP\n'
    
    invTotal=0
    retTotal=0
    invTamn=0
    retTamn=0
    ntTotal=0
    saleTotal=0
    netSoldTotal=0
    for records in records:

        retCount=0
        d_man_id=records[db.sm_invoice_head.d_man_id]
        if [s for s in dmanList if d_man_id in s]:
            index_element = dmanList.index(d_man_id)           
            retCount=invCList[index_element]
        d_man_id=records[db.sm_invoice_head.d_man_id]
        d_man_name=records[db.sm_invoice_head.d_man_name]
        noInvCount=records[db.sm_invoice_head.id.count()]
        invTotal=invTotal+records[db.sm_invoice_head.id.count()]
        
        retTotal=retTotal+retCount
        invAmn=(records[db.sm_invoice_head.actual_total_tp.sum()])
        
        invTamn=invTamn+invAmn
        
        retAmn=records[(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_sp_discount).sum()]
        
        retTamn=retTamn+retAmn
        sale=records[db.sm_invoice_head.actual_total_tp.sum()]
        netSold=records[db.sm_invoice_head.actual_total_tp.sum()]-retAmn
    
    
        saleTotal=saleTotal+sale
        netSoldTotal=netSoldTotal+netSold
        eP=(netSold*100)/sale
        rP=(retAmn*100)/sale
#         ntSTP=(records[db.sm_invoice_head.total_amount.sum()]+records[(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum()])-records[db.sm_invoice_head.vat_total_amount.sum()]
        
        ntTotal=ntTotal+(invAmn-retAmn)
        saleTotal=saleTotal+sale
        netSoldTotal=netSoldTotal+netSold
        ePTotal=(netSoldTotal*100)/saleTotal
        rPTotal=(retTamn*100)/saleTotal
         
               
        myString+=str(d_man_id)+','+str(d_man_name)+','+str(noInvCount)+','+str(retCount)+','+str(invAmn)+','+str(retAmn)+','+str(eP)+','+str(rP)+','+str(netSold)+'\n'
      
    myString+='\n\n,,'+str(invTotal)+','+str(retTotal)+','+str(invTamn)+','+str(retTamn)+','+str(ePTotal)+','+str(rPTotal)+','+str(ntTotal)+'\n'     
#     return myString
    
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=DeliveryPersonWiseSalesStatement.csv'   
    return str(myString) 

    
def dp_wise_sale_ssTPD():
    c_id=session.cid   
#     return c_id
    response.title='Delivery Person Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    dman_id=str(request.vars.dman_id).strip()
    dman_name=str(request.vars.dman_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  
#     return dman_id
        
#     if (dman_id==""):
#         session.flash="Please select deliery person."
#         redirect(URL(c='report_sales',f='home'))
        
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    qset_fr=db()
    qset_fr=qset_fr(db.sm_invoice_head.cid==c_id)
    qset_fr=qset_fr(db.sm_invoice_head.status=='Invoiced')
    qset_fr=qset_fr((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    qset_fr=qset_fr(db.sm_invoice_head.total_amount == ((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat)-(db.sm_invoice_head.return_discount+db.sm_invoice_head.return_sp_discount)))

    if (depot_id!=''):
        qset=qset(db.sm_invoice_head.depot_id==depot_id)
        qset_fr=qset_fr(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice_head.store_id==store_id)   
        qset_fr=qset_fr(db.sm_invoice_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_invoice_head.client_id==client_id)
        qset_fr=qset_fr(db.sm_invoice_head.client_id==client_id)
    if (teritory_id!=''):
        qset=qset(db.sm_invoice_head.area_id==teritory_id)
        qset_fr=qset_fr(db.sm_invoice_head.area_id==teritory_id)
    if (mso_id!=''):
        qset=qset(db.sm_invoice_head.rep_id==mso_id) 
        qset_fr=qset_fr(db.sm_invoice_head.rep_id==mso_id) 
    if (dman_id!=''):
        qset=qset(db.sm_invoice_head.d_man_id==dman_id)
        qset_fr=qset_fr(db.sm_invoice_head.d_man_id==dman_id) 
    if (market_id!=''):
        qset=qset(db.sm_invoice_head.market_id==market_id)
        qset_fr=qset_fr(db.sm_invoice_head.market_id==market_id)

        
    records=qset.select(db.sm_invoice_head.d_man_id,db.sm_invoice_head.d_man_name,db.sm_invoice_head.id.count(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.vat_total_amount.sum(),(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),(db.sm_invoice_head.return_discount+db.sm_invoice_head.return_sp_discount).sum(), orderby=db.sm_invoice_head.d_man_id,groupby=db.sm_invoice_head.d_man_id)
    records_fr=qset_fr.select(db.sm_invoice_head.d_man_id,db.sm_invoice_head.id.count(), orderby=db.sm_invoice_head.d_man_id,groupby=db.sm_invoice_head.d_man_id)
#     return records_fr
#     return db._lastsql
     
    dmanList=[]
    invCList=[]
    for records_fr in records_fr:
        dman_id = records_fr[db.sm_invoice_head.d_man_id]
        invCount = records_fr[db.sm_invoice_head.id.count()]
        dmanList.append(dman_id)
        invCList.append(invCount)
            
    
    #REmove , from record.Cause , means new column in excel    
    myString='Daterange,'+date_from+','+date_to+'\n'
    myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='Store,'+store_id+'|'+store_name+'\n'
    myString+='Teritory,'+teritory_id+'|'+teritory_name+'\n'
    myString+='DeliveryMan,'+dman_id+'|'+dman_name+'\n'
    myString+='Customer,'+customer_id+'|'+customer_name+'\n'
    myString+='MSO,'+mso_id+'|'+mso_name+'\n'
    myString+='Market,'+market_id+'|'+market_name+'\n\n'
    
   
        
    myString+='DP ID ,   Delivery Person Name ,   No of Inv.  ,  Full Return No  ,  Inv Amnt ,   Ret Amnt ,   Exec%  ,  Ret%  ,  Net Sold TP\n'
    
    invTotal=0
    retTotal=0
    invTamn=0
    retTamn=0
    ntTotal=0
    saleTotal=0
    netSoldTotal=0
    for records in records:
        retCount=0
        d_man_id=records[db.sm_invoice_head.d_man_id]
        if [s for s in dmanList if d_man_id in s]:
            index_element = dmanList.index(d_man_id)           
            retCount=invCList[index_element]
        d_man_id=records[db.sm_invoice_head.d_man_id]
        d_man_name=records[db.sm_invoice_head.d_man_name]
        noInvCount=records[db.sm_invoice_head.id.count()]
        invTotal=invTotal+records[db.sm_invoice_head.id.count()]
        retTotal=retTotal+retCount
        invAmn=(records[db.sm_invoice_head.total_amount.sum()]+records[(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum()])-records[db.sm_invoice_head.vat_total_amount.sum()]

        invTamn=invTamn+invAmn
        retAmn=records[db.sm_invoice_head.return_tp.sum()]
        retTamn=retTamn+retAmn
        sale=records[db.sm_invoice_head.total_amount.sum()]
        netSold=records[db.sm_invoice_head.total_amount.sum()]-retAmn
    
    
        saleTotal=saleTotal+sale
        netSoldTotal=netSoldTotal+netSold
        eP=(netSold*100)/sale
        rP=(retAmn*100)/sale
#         ntSTP=(records[db.sm_invoice_head.total_amount.sum()]+records[(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum()])-records[db.sm_invoice_head.vat_total_amount.sum()]
        
        ntTotal=ntTotal+(records[db.sm_invoice_head.total_amount.sum()]+records[(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum()])-records[db.sm_invoice_head.vat_total_amount.sum()]
        saleTotal=saleTotal+sale
        netSoldTotal=netSoldTotal+netSold
        ePTotal=(netSoldTotal*100)/saleTotal
        rPTotal=(retTamn*100)/saleTotal
         
               
        myString+=str(d_man_id)+','+str(d_man_name)+','+str(noInvCount)+','+str(retCount)+','+str(round(invAmn,2))+','+str(round(retAmn,2))+','+str(round(eP,2))+','+str(round(rP,2))+','+str(round(netSold,2))+'\n'
      
    myString+='\n\n,,'+str(invTotal)+','+str(retTotal)+','+str(round(invTamn,2))+','+str(round(retTamn,2))+','+str(round(ePTotal,2))+','+str(round(rPTotal,2))+','+str(round(ntTotal,2))+'\n'     
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=DeliveryPersonWiseSalesStatementTP.csv'   
    return str(myString) 
    
      
      
def salesClosingStockS():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    dman_id=str(request.vars.dman_id).strip()
    dman_name=str(request.vars.dman_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

        
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    qset=qset(db.sm_depot_stock_balance.store_id==store_id)
    qset=qset(db.sm_depot_stock_balance.quantity>0)
    
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)
    
       
    records=qset.select(db.sm_item.item_id,db.sm_item.name,db.sm_depot_stock_balance.quantity.sum(),(db.sm_depot_stock_balance.quantity * db.sm_item.price).sum(),db.sm_item.price,orderby=db.sm_item.name,groupby=db.sm_item.item_id)
    
    qset_inv=db()
    qset_inv=qset_inv(db.sm_invoice.cid==c_id)
    qset_inv=qset_inv(db.sm_invoice.depot_id==depot_id)
    qset_inv=qset_inv(db.sm_invoice.store_id==store_id)
    
    qset_inv=qset_inv(db.sm_invoice.status=='Invoiced')
    qset_inv=qset_inv((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
    records_inv=qset_inv.select(db.sm_invoice.item_id,db.sm_invoice.actual_tp,(db.sm_invoice.quantity+db.sm_invoice.bonus_qty).sum(),(db.sm_invoice.return_qty+db.sm_invoice.return_bonus_qty).sum(),((db.sm_invoice.quantity+db.sm_invoice.bonus_qty)-(db.sm_invoice.return_qty+db.sm_invoice.return_bonus_qty)).sum(),(db.sm_invoice.actual_tp*((db.sm_invoice.quantity+db.sm_invoice.bonus_qty)-(db.sm_invoice.return_qty+db.sm_invoice.return_bonus_qty))).sum(),orderby=db.sm_invoice.item_id,groupby=db.sm_invoice.item_id)
#     return db._lastsql
    itemList=[]
    itemQtyList=[]
    sateQtyList=[]
    retQtyList=[]
    itemSList=[]
    totalSaleTP=0
    for records_inv in records_inv:
        item_id = records_inv[db.sm_invoice.item_id]
        itemQty = records_inv[((db.sm_invoice.quantity+db.sm_invoice.bonus_qty)-(db.sm_invoice.return_qty+db.sm_invoice.return_bonus_qty)).sum()]
        
#         saleQty=records_inv[(db.sm_invoice.quantity+db.sm_invoice.bonus_qty).sum()]
#         retQty=records_inv[(db.sm_invoice.return_qty+db.sm_invoice.return_bonus_qty).sum()]
        
        itemS=records_inv[(db.sm_invoice.actual_tp*((db.sm_invoice.quantity+db.sm_invoice.bonus_qty)-(db.sm_invoice.return_qty+db.sm_invoice.return_bonus_qty))).sum()]
#         itemTP=records_inv[db.sm_invoice.actual_tp]
        totalSaleTP=totalSaleTP+itemS
        itemList.append(item_id)
        itemQtyList.append(itemQty)
        itemSList.append(itemS)
#         sateQtyList.append(saleQty)
#         retQtyList.append(retQty)
#         itemTPList.append(itemTP)
#     return totalTp
    qset_inv_note=db()
    qset_inv_note=qset_inv_note(db.sm_invoice.cid==c_id)
    qset_inv_note=qset_inv_note(db.sm_invoice.depot_id==depot_id)
    qset_inv_note=qset_inv_note(db.sm_invoice.store_id==store_id)
    
    qset_inv_note=qset_inv_note(db.sm_invoice.status=='Invoiced')
    qset_inv_note=qset_inv_note((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
    records_inv_note=qset_inv_note.select(db.sm_invoice.item_id,db.sm_invoice.actual_tp,(db.sm_invoice.quantity+db.sm_invoice.bonus_qty).sum(),orderby=db.sm_invoice.item_id,groupby=db.sm_invoice.item_id| db.sm_invoice.actual_tp)
#     return records_inv_note

    
    item_str=""
    item_past=''
    for records_inv_note in records_inv_note:
        item_id = records_inv_note[db.sm_invoice.item_id]
        itemQty = records_inv_note[(db.sm_invoice.quantity+db.sm_invoice.bonus_qty).sum()]
        itemTP = records_inv_note[db.sm_invoice.actual_tp]
        
        if item_past!=item_id:           
           item_str=item_str+"Item"+str(item_id)
           note=""
           tp=""
        if tp=='':
            tp=str(itemTP)  
        else:
            tp=tp+','+str(itemTP) 
        if note=='':
            note="("+str(itemTP)+"*"+str(itemQty)+")" 
        else:
            note=note+'+'+"("+str(itemTP)+"*"+str(itemQty)+")"
        
        item_str=item_str+"TP"+tp+"Note"+note
        
        item_past=item_id
             
    return dict(records=records,itemList=itemList,itemQtyList=itemQtyList,itemSList=itemSList,item_str=item_str,totalSaleTP=totalSaleTP,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  teritory_id=teritory_id, teritory_name=teritory_name, dman_id=dman_id,dman_name=dman_name, mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name)

def salesClosingStockSD():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    dman_id=str(request.vars.dman_id).strip()
    dman_name=str(request.vars.dman_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

        
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    qset=qset(db.sm_depot_stock_balance.store_id==store_id)
    qset=qset(db.sm_depot_stock_balance.quantity>0)
    
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)
    
       
    records=qset.select(db.sm_item.item_id,db.sm_item.name,db.sm_depot_stock_balance.quantity.sum(),(db.sm_depot_stock_balance.quantity * db.sm_item.price).sum(),db.sm_item.price,orderby=db.sm_item.name,groupby=db.sm_item.item_id)
    
    qset_inv=db()
    qset_inv=qset_inv(db.sm_invoice.cid==c_id)
    qset_inv=qset_inv(db.sm_invoice.depot_id==depot_id)
    qset_inv=qset_inv(db.sm_invoice.store_id==store_id)
    
    qset_inv=qset_inv(db.sm_invoice.status=='Invoiced')
    qset_inv=qset_inv((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
    records_inv=qset_inv.select(db.sm_invoice.item_id,db.sm_invoice.actual_tp,(db.sm_invoice.quantity+db.sm_invoice.bonus_qty).sum(),(db.sm_invoice.return_qty+db.sm_invoice.return_bonus_qty).sum(),((db.sm_invoice.quantity+db.sm_invoice.bonus_qty)-(db.sm_invoice.return_qty+db.sm_invoice.return_bonus_qty)).sum(),(db.sm_invoice.actual_tp*((db.sm_invoice.quantity+db.sm_invoice.bonus_qty)-(db.sm_invoice.return_qty+db.sm_invoice.return_bonus_qty))).sum(),orderby=db.sm_invoice.item_id,groupby=db.sm_invoice.item_id)
#     return db._lastsql
    itemList=[]
    itemQtyList=[]
    sateQtyList=[]
    retQtyList=[]
    itemSList=[]
    totalSaleTP=0
    for records_inv in records_inv:
        item_id = records_inv[db.sm_invoice.item_id]
        itemQty = records_inv[((db.sm_invoice.quantity+db.sm_invoice.bonus_qty)-(db.sm_invoice.return_qty+db.sm_invoice.return_bonus_qty)).sum()]
        
#         saleQty=records_inv[(db.sm_invoice.quantity+db.sm_invoice.bonus_qty).sum()]
#         retQty=records_inv[(db.sm_invoice.return_qty+db.sm_invoice.return_bonus_qty).sum()]
        
        itemS=records_inv[(db.sm_invoice.actual_tp*((db.sm_invoice.quantity+db.sm_invoice.bonus_qty)-(db.sm_invoice.return_qty+db.sm_invoice.return_bonus_qty))).sum()]
#         itemTP=records_inv[db.sm_invoice.actual_tp]
        totalSaleTP=totalSaleTP+itemS
        itemList.append(item_id)
        itemQtyList.append(itemQty)
        itemSList.append(itemS)
#         sateQtyList.append(saleQty)
#         retQtyList.append(retQty)
#         itemTPList.append(itemTP)
#     return totalTp
    qset_inv_note=db()
    qset_inv_note=qset_inv_note(db.sm_invoice.cid==c_id)
    qset_inv_note=qset_inv_note(db.sm_invoice.depot_id==depot_id)
    qset_inv_note=qset_inv_note(db.sm_invoice.store_id==store_id)
    
    qset_inv_note=qset_inv_note(db.sm_invoice.status=='Invoiced')
    qset_inv_note=qset_inv_note((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
    records_inv_note=qset_inv_note.select(db.sm_invoice.item_id,db.sm_invoice.actual_tp,(db.sm_invoice.quantity+db.sm_invoice.bonus_qty).sum(),orderby=db.sm_invoice.item_id,groupby=db.sm_invoice.item_id| db.sm_invoice.actual_tp)
#     return records_inv_note

    
    item_str=""
    item_past=''
    for records_inv_note in records_inv_note:
        item_id = records_inv_note[db.sm_invoice.item_id]
        itemQty = records_inv_note[(db.sm_invoice.quantity+db.sm_invoice.bonus_qty).sum()]
        itemTP = records_inv_note[db.sm_invoice.actual_tp]
        
        if item_past!=item_id:           
           item_str=item_str+"Item"+str(item_id)
           note=""
           tp=""
        if tp=='':
            tp=str(itemTP)  
        else:
            tp=tp+','+str(itemTP) 
        if note=='':
            note="("+str(itemTP)+"*"+str(itemQty)+")" 
        else:
            note=note+'+'+"("+str(itemTP)+"*"+str(itemQty)+")"
        
        item_str=item_str+"TP"+tp+"Note"+note
        
        item_past=item_id
         
        
            
#CSV  
    myString='DateRange,'+date_from+'-'+date_to+'\n'
    myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='Store,'+store_id+'|'+store_name+'\n\n\n'
    

        
    myString+='Item  ,  ItemName  ,  SalesTP   , SalesS.Qty  ,  SalesTP*S.Qty   , Notes  ,  SalesSClosing stock Qty   , StockTP  ,  StockTP*Closing stock Qty\n'
    
    totalStockTP=0
    for record in records:
        item_id =record[db.sm_item.item_id]
        itemQty=0
        itemS=0
    
        if [s for s in itemList if item_id in s]:
            index_element = itemList.index(item_id)
            itemQty=itemQtyList[index_element]
            itemS=itemSList[index_element]
        
        item_idF="Item"+str(record[db.sm_item.item_id]+"TP")
        tp=''
        Note=''
        item_str_get=''
        if (item_str.find(item_idF)!=-1):
            item_str_get=item_str.split(item_idF)[1].split("Item")[0] 
            item_strList= item_str_get.split("TP")
            for i in range(len(item_strList)):
                tp=item_strList[i].split("Note")[0].replace(',','/')
                Note=item_strList[i].split("Note")[1].replace(',','')

        
      
        totalStockTP=totalStockTP + record[(db.sm_depot_stock_balance.quantity * db.sm_item.price).sum()]
        myString+=str(record[db.sm_item.item_id])+','+str(record[db.sm_item.name])+','+str(tp)+','+str(itemQty)+','+str(round(itemS))+','+str(Note)+','+str(record[db.sm_depot_stock_balance.quantity.sum()])+','+str(record[db.sm_item.price])+','+str(round(record[(db.sm_depot_stock_balance.quantity * db.sm_item.price).sum()]))+'\n\n'
    myString+=',,,,'+str(totalSaleTP)+',,,,'+str(totalStockTP)+'\n'
              
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=salesClosingStockS.csv'   
    return str(myString)    
    

def salesClosingStockSB():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    dman_id=str(request.vars.dman_id).strip()
    dman_name=str(request.vars.dman_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

        
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    qset=qset(db.sm_depot_stock_balance.store_id==store_id)
    qset=qset(db.sm_depot_stock_balance.quantity>0)
    
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)
    
       
    records=qset.select(db.sm_item.item_id,db.sm_item.name,db.sm_depot_stock_balance.quantity.sum(),db.sm_item.price,(db.sm_depot_stock_balance.quantity*db.sm_item.price).sum(),orderby=db.sm_item.name,groupby=db.sm_item.item_id)
    itemList=[]
    itemQtyList=[]
    itemTPList=[]
    stTPList=[]
    totalSTP=0
    for records in records:
        item_id = records[db.sm_item.item_id]
        itemQty = records[db.sm_depot_stock_balance.quantity.sum()]
        itemP=records[db.sm_item.price]
        stTP=records[(db.sm_depot_stock_balance.quantity*db.sm_item.price).sum()]
        totalSTP=totalSTP+stTP
        itemList.append(item_id)
        itemQtyList.append(itemQty)
        itemTPList.append(itemP)
        stTPList.append(stTP)
    qset_inv=db()
    qset_inv=qset_inv(db.sm_invoice.cid==c_id)
    qset_inv=qset_inv(db.sm_invoice.depot_id==depot_id)
    qset_inv=qset_inv(db.sm_invoice.store_id==store_id)
    
    qset_inv=qset_inv(db.sm_invoice.status=='Invoiced')
    qset_inv=qset_inv((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
    records_inv=qset_inv.select(db.sm_invoice.item_id,db.sm_invoice.item_name,db.sm_invoice.actual_tp,((db.sm_invoice.quantity+db.sm_invoice.bonus_qty)-(db.sm_invoice.return_qty+db.sm_invoice.return_bonus_qty)).sum(),(db.sm_invoice.actual_tp*db.sm_invoice.quantity).sum(),orderby=db.sm_invoice.item_name | db.sm_invoice.actual_tp,groupby=db.sm_invoice.item_id | db.sm_invoice.actual_tp)
   
   
   
    
    return dict(records_inv=records_inv,itemList=itemList,itemQtyList=itemQtyList,itemTPList=itemTPList,stTPList=stTPList,totalSTP=totalSTP,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  teritory_id=teritory_id, teritory_name=teritory_name, dman_id=dman_id,dman_name=dman_name, mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name)

def salesClosingStockSBD():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    dman_id=str(request.vars.dman_id).strip()
    dman_name=str(request.vars.dman_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

        
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    qset=qset(db.sm_depot_stock_balance.store_id==store_id)
    qset=qset(db.sm_depot_stock_balance.quantity>0)
    
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)
    
       
    records=qset.select(db.sm_item.item_id,db.sm_item.name,db.sm_depot_stock_balance.quantity.sum(),db.sm_item.price,(db.sm_depot_stock_balance.quantity*db.sm_item.price).sum(),orderby=db.sm_item.name,groupby=db.sm_item.item_id)
    itemList=[]
    itemQtyList=[]
    itemTPList=[]
    stTPList=[]
    totalSTP=0
    for records in records:
        item_id = records[db.sm_item.item_id]
        itemQty = records[db.sm_depot_stock_balance.quantity.sum()]
        itemP=records[db.sm_item.price]
        stTP=records[(db.sm_depot_stock_balance.quantity*db.sm_item.price).sum()]
        totalSTP=totalSTP+stTP
        itemList.append(item_id)
        itemQtyList.append(itemQty)
        itemTPList.append(itemP)
        stTPList.append(stTP)
    qset_inv=db()
    qset_inv=qset_inv(db.sm_invoice.cid==c_id)
    qset_inv=qset_inv(db.sm_invoice.depot_id==depot_id)
    qset_inv=qset_inv(db.sm_invoice.store_id==store_id)
    
    qset_inv=qset_inv(db.sm_invoice.status=='Invoiced')
    qset_inv=qset_inv((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
    records_inv=qset_inv.select(db.sm_invoice.item_id,db.sm_invoice.item_name,db.sm_invoice.actual_tp,((db.sm_invoice.quantity+db.sm_invoice.bonus_qty)-(db.sm_invoice.return_qty+db.sm_invoice.return_bonus_qty)).sum(),(db.sm_invoice.actual_tp*db.sm_invoice.quantity).sum(),orderby=db.sm_invoice.item_name | db.sm_invoice.actual_tp,groupby=db.sm_invoice.item_id | db.sm_invoice.actual_tp)

    #CSV  
    myString='DateRange,'+date_from+'-'+date_to+'\n'
    myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='Store,'+store_id+'|'+store_name+'\n\n\n'
    myString+='Item  ,  ItemName  ,  SalesTP   , SalesS.Qty  ,  SalesTP*S.Qty  ,  SalesSClosing stock Qty   , StockTP  ,  StockTP*Closing stock Qty\n'
    
    totalSaleTP=0
    for records_inv in records_inv:
        item_id =records_inv[db.sm_invoice.item_id]
        itemQty=0
        itemS=0
    
        if [s for s in itemList if item_id in s]:
              index_element = itemList.index(item_id)
              itemQty=itemQtyList[index_element]
              itemTP=itemTPList[index_element]
              stTP=stTPList[index_element]
        
        
        totalSaleTP=totalSaleTP+records_inv[(db.sm_invoice.actual_tp*db.sm_invoice.quantity).sum()]
        myString+=str(records_inv[db.sm_invoice.item_id])+','+str(records_inv[db.sm_invoice.item_name])+','+str(records_inv[db.sm_invoice.actual_tp])+','+str(records_inv[((db.sm_invoice.quantity+db.sm_invoice.bonus_qty)-(db.sm_invoice.return_qty+db.sm_invoice.return_bonus_qty)).sum()])+','+str(records_inv[(db.sm_invoice.actual_tp*db.sm_invoice.quantity).sum()])+','+str(itemQty)+','+str(itemTP)+','+str(stTP)+'\n\n'
    myString+=',,,,'+str(totalSaleTP)+',,,'+str(totalSTP)+'\n'
              
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=salesClosingStockSB.csv'   
    return str(myString)    
        
        
        
        
# ==========================Sales Comparision===========================    
def msoSCTop():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

        
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.quantity>0)
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)      
    if (depot_id!=''):
        qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_depot_stock_balance.store_id==store_id) 
    records=qset.select(db.sm_item.item_id,db.sm_item.name,db.sm_item.category_id,db.sm_depot_stock_balance.quantity.sum(),db.sm_item.price,orderby=db.sm_item.name,groupby=db.sm_item.item_id)
    prodDict={}
    prodList=[]
    for record in records:
        item_id= record[db.sm_item.item_id]
        item_name= record[db.sm_item.name]
        category_id = record[db.sm_item.category_id]
        stockBalance = record[db.sm_depot_stock_balance.quantity.sum()]
        TP= record[db.sm_item.price]
        
        prodDict={'item_id':item_id,'item_name':item_name,'category_id':category_id,'stockBalance':stockBalance,'TP':TP}
        prodList.append(prodDict)
    
    
#     Summary
    qset_sum=db()
    qset_sum=qset_sum(db.sm_invoice.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice.status=='Invoiced')
    qset_sum=qset_sum((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
    if (depot_id!=''):
        qset_sum=qset_sum(db.sm_invoice.depot_id==depot_id)
    if (store_id!=''):
        qset_sum=qset_sum(db.sm_invoice.store_id==store_id)                  
    records_sum=qset_sum.select(db.sm_invoice.item_id,db.sm_invoice.category_id,db.sm_invoice.level1_id,db.sm_invoice.level2_id,db.sm_invoice.level3_id,db.sm_invoice.level1_name,db.sm_invoice.level2_name,db.sm_invoice.level3_name  ,(db.sm_invoice.quantity+db.sm_invoice.bonus_qty).sum(), orderby=db.sm_invoice.item_id | db.sm_invoice.category_id |db.sm_invoice.level1_id|db.sm_invoice.level2_id|db.sm_invoice.level3_id,groupby=db.sm_invoice.level1_id|db.sm_invoice.level2_id|db.sm_invoice.level3_id |db.sm_invoice.item_id | db.sm_invoice.category_id)
    
    invDict={}
    invList=[]
    itemList=[]
    for records_sum in records_sum:
        item_id= records_sum[db.sm_invoice.item_id]
        category_id = records_sum[db.sm_invoice.category_id]
        itemQty = records_sum[(db.sm_invoice.quantity+db.sm_invoice.bonus_qty).sum()]
        rsm= records_sum[db.sm_invoice.level1_id]
        fm= records_sum[db.sm_invoice.level2_id]
        tr= records_sum[db.sm_invoice.level3_id]
        itemList.append(item_id)
        invDict={'item_id':item_id,'category_id':category_id,'itemQty':itemQty,'rsm':rsm,'fm':fm,'tr':tr}
        invList.append(invDict)
    return dict(records=records,invList=invList,itemList=itemList,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name)


def msoSCTopD():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

        
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.quantity>0)
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)      
    if (depot_id!=''):
        qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_depot_stock_balance.store_id==store_id) 
    records=qset.select(db.sm_item.item_id,db.sm_item.name,db.sm_item.category_id,db.sm_depot_stock_balance.quantity.sum(),db.sm_item.price,orderby=db.sm_item.name,groupby=db.sm_item.item_id)
    prodDict={}
    prodList=[]
    for record in records:
        item_id= record[db.sm_item.item_id]
        item_name= record[db.sm_item.name]
        category_id = record[db.sm_item.category_id]
        stockBalance = record[db.sm_depot_stock_balance.quantity.sum()]
        TP= record[db.sm_item.price]
        
        prodDict={'item_id':item_id,'item_name':item_name,'category_id':category_id,'stockBalance':stockBalance,'TP':TP}
        prodList.append(prodDict)
    
    
#     Summary
    qset_sum=db()
    qset_sum=qset_sum(db.sm_invoice.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice.status=='Invoiced')
    qset_sum=qset_sum((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
    if (depot_id!=''):
        qset_sum=qset_sum(db.sm_invoice.depot_id==depot_id)
    if (store_id!=''):
        qset_sum=qset_sum(db.sm_invoice.store_id==store_id)                  
    records_sum=qset_sum.select(db.sm_invoice.item_id,db.sm_invoice.category_id,db.sm_invoice.level1_id,db.sm_invoice.level2_id,db.sm_invoice.level3_id,db.sm_invoice.level1_name,db.sm_invoice.level2_name,db.sm_invoice.level3_name  ,(db.sm_invoice.quantity+db.sm_invoice.bonus_qty).sum(), orderby=db.sm_invoice.item_id | db.sm_invoice.category_id |db.sm_invoice.level1_id|db.sm_invoice.level2_id|db.sm_invoice.level3_id,groupby=db.sm_invoice.level1_id|db.sm_invoice.level2_id|db.sm_invoice.level3_id |db.sm_invoice.item_id | db.sm_invoice.category_id)
    
    invDict={}
    invList=[]
    itemList=[]
    for records_sum in records_sum:
        item_id= records_sum[db.sm_invoice.item_id]
        category_id = records_sum[db.sm_invoice.category_id]
        itemQty = records_sum[(db.sm_invoice.quantity+db.sm_invoice.bonus_qty).sum()]
        rsm= records_sum[db.sm_invoice.level1_id]
        fm= records_sum[db.sm_invoice.level2_id]
        tr= records_sum[db.sm_invoice.level3_id]
        itemList.append(item_id)
        invDict={'item_id':item_id,'category_id':category_id,'itemQty':itemQty,'rsm':rsm,'fm':fm,'tr':tr}
        invList.append(invDict)
    
#     CSV
    #REmove , from record.Cause , means new column in excel    
    myString='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='Store,'+store_id+'|'+store_name+'\n\n'
    
    
    
        
    myString+='Item   , ItemName ,   TP ,   Stock ,   RSM  ,  FM  ,  TR ,   A  ,  B  ,  C  ,  Bonus\n'
    
    
    pastItem=''
    pastRsm=''
    pastFm=''
    pastTr=''
    for records in records:
        item_id=records[db.sm_item.item_id]
        if [s for s in itemList if item_id in s]:
            index_element = itemList.index(item_id)           
            itemCount= itemList.count(item_id)    
            c=index_element
            while c < index_element+itemCount: 
                qtyA=0
                qtyB=0
                qtyC=0  
                qtyBonus=0
                if invList[c]['category_id']=='A':
                    qtyA=str(invList[c]['itemQty'])
                elif invList[c]['category_id']=='B':
                    qtyB=str(invList[c]['itemQty'])
                elif invList[c]['category_id']=='C':
                    qtyC=str(invList[c]['itemQty'])
                elif invList[c]['category_id']=='BONUS':
                    qtyBonus=str(invList[c]['itemQty']) 
#                 if pastItem!=records[db.sm_item.item_id]:
#                     myString=myString+'\n'
                myString=myString+str(records[db.sm_item.item_id])+','+str(records[db.sm_item.name])+','+str(records[db.sm_item.price])+','+str(records[db.sm_depot_stock_balance.quantity.sum()])+','+str(invList[c]['rsm']) +','+str(invList[c]['fm'])+','+str(invList[c]['tr'])+','+str(qtyA)+','+str(qtyB) +','+str(qtyC)+','+str(qtyBonus)                   
                pastItem=records[db.sm_item.item_id]
                pastRsm=invList[c]['rsm']
                pastFm=invList[c]['fm']
                pastTr=invList[c]['tr']
                c=c+1
                myString=myString+'\n'

         
         
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=msoSCTop.csv'   
    return str(myString) 
    
    
    
    return dict(records=records,invList=invList,itemList=itemList,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name)

def msoSCTopSum():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

        
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.quantity>0)
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)      
    if (depot_id!=''):
        qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_depot_stock_balance.store_id==store_id) 
    records=qset.select(db.sm_item.item_id,db.sm_item.name,db.sm_item.category_id,db.sm_depot_stock_balance.quantity.sum(),db.sm_item.price,orderby=db.sm_item.category_id,groupby=db.sm_item.category_id)
#     prodDict={}
#     prodList=[]
#     prodcatList=[]
#     for record in records:
#         item_id= record[db.sm_item.item_id]
#         item_name= record[db.sm_item.name]
#         category_id = record[db.sm_item.category_id]
#         stockBalance = record[db.sm_depot_stock_balance.quantity.sum()]
#         TP= record[db.sm_item.price]
#          
#         prodDict={'item_id':item_id,'item_name':item_name,'category_id':category_id,'stockBalance':stockBalance,'TP':TP}
#         prodList.append(prodDict)
#         prodcatList.append(category_id)
    
    
#     Summary
    qset_sum=db()
    qset_sum=qset_sum(db.sm_invoice.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice.status=='Invoiced')
    qset_sum=qset_sum((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
    if (depot_id!=''):
        qset_sum=qset_sum(db.sm_invoice.depot_id==depot_id)
    if (store_id!=''):
        qset_sum=qset_sum(db.sm_invoice.store_id==store_id)                  
    records_sum=qset_sum.select(db.sm_invoice.category_id,db.sm_invoice.level1_id,db.sm_invoice.level2_id,db.sm_invoice.level3_id,db.sm_invoice.level1_name,db.sm_invoice.level2_name,db.sm_invoice.level3_name  ,(db.sm_invoice.quantity+db.sm_invoice.bonus_qty).sum(), orderby=db.sm_invoice.level1_id|db.sm_invoice.level2_id|db.sm_invoice.level3_id|db.sm_invoice.category_id ,groupby=db.sm_invoice.level1_id|db.sm_invoice.level2_id|db.sm_invoice.level3_id | db.sm_invoice.category_id)
#     return records_sum
    invDict={}
    invList=[]
    itemList=[]
    qtyA=0
    qtyB=0
    qtyC=0
    qtyBonus=0
    tr_past=''
    qty_str1=''
    qty_str=''
    for record_sum in records_sum:
        category_id = record_sum[db.sm_invoice.category_id]
        itemQty = record_sum[(db.sm_invoice.quantity+db.sm_invoice.bonus_qty).sum()]
        rsm= record_sum[db.sm_invoice.level1_id]
        fm= record_sum[db.sm_invoice.level2_id]
        tr= record_sum[db.sm_invoice.level3_id]
        if category_id=='A':
            qtyA=itemQty
        if category_id=='B':
            qtyA=itemQty
        if category_id=='C':
            qtyA=itemQty
        if category_id=='BONUS':
            qtyA=itemQty
            
        itemList.append(category_id)
        
        if tr_past!=tr :
                qty_str=qty_str+'<fdrd>'+str(tr)
        qty_str=qty_str+str(qtyA)+','+str(qtyB)+','+str(qtyC)+','+str(qtyBonus)+'<rd>'        
        
        tr_past=tr
        
        
        
        
        
        
#     return qty_str
        
#         if tr_past!=tr:
#             if tr_past!='':
#                 qty_str1=
#                 invDict={'category_id':category_id,'qtyA':qtyA,'qtyB':qtyB,'qtyC':qtyC,'qtyA':qtyA,'rsm':rsm,'fm':fm,'tr':tr}
#                 invList.append(invDict)
    
        
    return dict(records_sum=records_sum,qty_str=qty_str,invList=invList,itemList=itemList,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name)
 
def msoSC():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

        
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    qset=qset(db.sm_depot_stock_balance.store_id==store_id)
    qset=qset(db.sm_depot_stock_balance.quantity>0)
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)      
    records=qset.select(db.sm_item.item_id,db.sm_item.name,db.sm_item.category_id,db.sm_depot_stock_balance.quantity.sum(),db.sm_item.price,orderby=db.sm_item.name,groupby=db.sm_item.item_id)
    
    
    qset_tr=db()
    qset_tr=qset_tr(db.sm_invoice.cid==c_id)
    qset_tr=qset_tr(db.sm_invoice.depot_id==depot_id)
    qset_tr=qset_tr(db.sm_invoice.store_id==store_id)
    qset_tr=qset_tr(db.sm_invoice.status=='Invoiced')
    qset_tr=qset_tr((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
    records_tr=qset_tr.select(db.sm_invoice.area_id ,db.sm_invoice.item_id,db.sm_invoice.category_id,(db.sm_invoice.quantity+db.sm_invoice.bonus_qty).sum(),orderby=db.sm_invoice.area_id ,groupby=db.sm_invoice.area_id )
#     return records_tr
    
    
    qset_inv=db()
    qset_inv=qset_inv(db.sm_invoice.cid==c_id)
    qset_inv=qset_inv(db.sm_invoice.depot_id==depot_id)
    qset_inv=qset_inv(db.sm_invoice.store_id==store_id)
    qset_inv=qset_inv(db.sm_invoice.status=='Invoiced')
    qset_inv=qset_inv((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
    records_inv=qset_inv.select(db.sm_invoice.area_id ,db.sm_invoice.item_id,db.sm_invoice.category_id,(db.sm_invoice.quantity+db.sm_invoice.bonus_qty).sum(),orderby=db.sm_invoice.area_id | db.sm_invoice.item_id | db.sm_invoice.category_id,groupby=db.sm_invoice.area_id | db.sm_invoice.item_id | db.sm_invoice.category_id)

    itemList=[]
    itemQtyDict={}
    itemQtyList=[]
   

    for records_inv in records_inv:
        tr= records_inv[db.sm_invoice.area_id]
        item_id = records_inv[db.sm_invoice.item_id]
        itemQty = records_inv[(db.sm_invoice.quantity+db.sm_invoice.bonus_qty).sum()]
        itemCategory = records_inv[db.sm_invoice.category_id]

        itemList.append(str(item_id)+"-"+str(itemCategory))
        
        itemQtyDict={'tr':tr , 'item':item_id , 'category':  itemCategory,'qty':itemQty}  
        itemQtyList.append(itemQtyDict)



    return dict(records=records,itemList=itemList,records_inv=records_inv,records_tr=records_tr,itemQtyList=itemQtyList,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name)

# ============================================
def scNational():
    c_id=session.cid   
#     return c_id
    response.title='NationalSummary'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    tr_id=str(request.vars.tr_id).strip()
    tr_name=str(request.vars.tr_name).strip()
    
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

  


    conditionH=''
    if (depot_id!=''):
        conditionH=conditionH+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        conditionH=conditionH+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        conditionH=conditionH+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        conditionH=conditionH+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        conditionH=conditionH+"AND level3_id = '"+str(tr_id)+"'"
        
        
        
        
        
    dateRecordsH="SELECT  level0_id, count(DISTINCT  sl) as invcount FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+conditionH+" GROUP BY level0_id ORDER BY level0_id;"
#     return dateRecordsH
    records_head=db.executesql(dateRecordsH,as_dict = True) 
    
    rsmList=[]
    invCountList=[]
    for records_head in records_head:
        rsmList.append(records_head['level0_id'])
        invCountList.append(records_head['invcount'])


    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"

    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        condition=condition+"AND level3_id = '"+str(tr_id)+"'"

    dateRecords="SELECT category_id, level0_id, SUM((quantity - return_qty) * actual_tp) as amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY level0_id, category_id ORDER BY level0_id, category_id;"
#     return dateRecords
    records=db.executesql(dateRecords,as_dict = True) 
#     return records
    cat_str=''
    rsm_past=''
    
    totalAmount=0
    amnt=0
    
    for i in range(len(records)):
        record=records[i]
        
        category_id=record['category_id']
        amnt=record['amnt']
        if rsm_past!=record['level0_id']:
            cat_str=cat_str+'<fdrd'+str(record['level0_id'])+'>'
            amnA='0'
            amnB='0'
            amnC='0'
        if category_id=='A':
            amnA=str(amnt)
        if category_id=='B':
            amnB=str(amnt)
        if category_id=='C':
            amnC=str(amnt)
        cat_str=cat_str+amnA+','+amnB+','+amnC+'<rd>'
        rsm_past=record['level0_id']
#     return cat_str
    return dict(records=records,rsmList=rsmList,invCountList=invCountList,cat_str=cat_str,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name)

def scNationalD():
    c_id=session.cid   
#     return c_id
    response.title='NationalSummary'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    tr_id=str(request.vars.tr_id).strip()
    tr_name=str(request.vars.tr_name).strip()
    
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

  
    conditionH=''
    if (depot_id!=''):
        conditionH=conditionH+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        conditionH=conditionH+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        conditionH=conditionH+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        conditionH=conditionH+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        conditionH=conditionH+"AND level3_id = '"+str(tr_id)+"'"
    dateRecordsH="SELECT  level0_id, count(DISTINCT  sl) as invcount FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+conditionH+" GROUP BY level0_id ORDER BY level0_id;"
#     return dateRecordsH
    records_head=db.executesql(dateRecordsH,as_dict = True) 
    
    rsmList=[]
    invCountList=[]
    for records_head in records_head:
        rsmList.append(records_head['level0_id'])
        invCountList.append(records_head['invcount'])


    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
#         qset_sum=qset_sum(db.sm_invoice.depot_id==depot_id)
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        condition=condition+"AND level3_id = '"+str(tr_id)+"'"

    dateRecords="SELECT category_id, level0_id, SUM((quantity - return_qty) * actual_tp) as amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY level0_id, category_id ORDER BY level0_id, category_id;"
#     return dateRecords
    records=db.executesql(dateRecords,as_dict = True) 
#     return records
    cat_str=''
    rsm_past=''
    amnA='0'
    amnB='0'
    amnC='0'
    totalAmount=0
    amnt=0
    myString='Date Range,'+date_from+'to'+date_to+'\n'
    myString='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='Store,'+store_id+'|'+store_name+'\n'
    myString+='RSM,'+rsm_id+'|'+rsm_name+'\n'
    myString+='FM,'+fm_id+'|'+fm_name+'\n'
    myString+='TR,'+tr_id+'|'+tr_name+'\n\n\n'
    
    myString+='Zone ,   InvCount  ,  Total TP  ,TP A  ,  TP B  ,  TPC\n'
    for i in range(len(records)):
        record=records[i]
        category_id=record['category_id']
        amnt=record['amnt']
        if rsm_past!=record['level0_id']:
            cat_str=cat_str+'<fdrd'+str(record['level0_id'])+'>'
        if category_id=='A':
            amnA=str(amnt)
        if category_id=='B':
            amnB=str(amnt)
        if category_id=='C':
            amnC=str(amnt)
        cat_str=cat_str+amnA+','+amnB+','+amnC+'<rd>'
        rsm_past=record['level0_id']
#     return cat_str
#     strShow=''
    pastRsm=''
    ATotal=0
    BTotal=0
    CTotal=0
    Total=0
    for i in range(len(records)):  
        record=records[i]  
        spStr='<fdrd'+str(record['level0_id'])+'>'
        rsmStr=cat_str.split(spStr)[1].split('<fdrd')[0]
        rsmStrList=rsmStr.split('<rd>')
        i=0
        while i < len(rsmStrList)-1:
            amnA='0'
            amnB='0'
            amnC='0'
            catA=rsmStrList[i].split(',')[0]
            catB=rsmStrList[i].split(',')[1]
            catC=rsmStrList[i].split(',')[2]
            i=i+1
        
        ATotal=ATotal+float(catA)
        BTotal=BTotal+float(catB)
        CTotal=CTotal+float(catC)
        Total=float(catA)+float(catB)+float(catC)
    
    
# ===========     
        
        rsm=record['level0_id']
        invCount=0
        if [s for s in rsmList if rsm in s]:
            index_element = rsmList.index(rsm)           
            invCount= invCountList[index_element]
        
        if pastRsm!=record['level0_id']:
            myString+=str(record['level0_id'])+','+str(invCount)+','+str(Total)+','+str(ATotal)+','+str(BTotal)+','+str(CTotal)+'\n'
#         strShow= strShow+' past:'+str(pastRsm)+' rec:'+str(record['level0_id']) 
        pastRsm= record['level0_id']
#     return strShow
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=NationalSummary.csv'   
    return str(myString)
    
    
    
# =============================================================
def scRsm():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    tr_id=str(request.vars.tr_id).strip()
    tr_name=str(request.vars.tr_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

  
    conditionH=''
    if (depot_id!=''):
        conditionH=conditionH+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        conditionH=conditionH+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        conditionH=conditionH+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        conditionH=conditionH+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        conditionH=conditionH+"AND level3_id = '"+str(tr_id)+"'"    
        
        
    dateRecordsH="SELECT  level1_id, count(DISTINCT  sl) as invcount FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+conditionH+" GROUP BY level1_id ORDER BY level1_id;"
#     return dateRecordsH
    records_head=db.executesql(dateRecordsH,as_dict = True) 
    
    rsmList=[]
    invCountList=[]
    for records_head in records_head:
        rsmList.append(records_head['level1_id'])
        invCountList.append(records_head['invcount'])


    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"

    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        condition=condition+"AND level3_id = '"+str(tr_id)+"'"
  
    dateRecords="SELECT category_id, level1_id, SUM((quantity - return_qty) * actual_tp) as amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY level1_id, category_id ORDER BY level1_id, category_id;"
#     return dateRecords
    records=db.executesql(dateRecords,as_dict = True) 
#     return records
    cat_str=''
    rsm_past=''
    
    totalAmount=0
    amnt=0
    
    for i in range(len(records)):
        record=records[i]
        
        category_id=record['category_id']
        amnt=record['amnt']
        if rsm_past!=record['level1_id']:
            cat_str=cat_str+'<fdrd'+str(record['level1_id'])+'>'
            amnA='0'
            amnB='0'
            amnC='0'
        if category_id=='A':
            amnA=str(amnt)
        if category_id=='B':
            amnB=str(amnt)
        if category_id=='C':
            amnC=str(amnt)
        cat_str=cat_str+amnA+','+amnB+','+amnC+'<rd>'
        rsm_past=record['level1_id']
#     return cat_str
    return dict(records=records,rsmList=rsmList,invCountList=invCountList,cat_str=cat_str,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name)
# ========================
def scRsmD():
    c_id=session.cid   
    response.title='RSMSummary'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    tr_id=str(request.vars.tr_id).strip()
    tr_name=str(request.vars.tr_name).strip()
    
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

  
    conditionH=''
    if (depot_id!=''):
        conditionH=conditionH+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        conditionH=conditionH+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        conditionH=conditionH+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        conditionH=conditionH+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        conditionH=conditionH+"AND level3_id = '"+str(tr_id)+"'"
    
    dateRecordsH="SELECT  level1_id, count(DISTINCT  sl) as invcount FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+conditionH+" GROUP BY level1_id ORDER BY level1_id;"
#     return dateRecordsH
    records_head=db.executesql(dateRecordsH,as_dict = True) 
    
    rsmList=[]
    invCountList=[]
    for records_head in records_head:
        rsmList.append(records_head['level1_id'])
        invCountList.append(records_head['invcount'])


    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        condition=condition+"AND level3_id = '"+str(tr_id)+"'"

    dateRecords="SELECT category_id, level0_id, level1_id , SUM((quantity - return_qty) * actual_tp) as amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY level1_id, category_id ORDER BY level1_id, category_id;"

    records=db.executesql(dateRecords,as_dict = True) 

    cat_str=''
    rsm_past=''
    amnA='0'
    amnB='0'
    amnC='0'
    totalAmount=0
    amnt=0
    myString='Date Range,'+date_from+'to'+date_to+'\n'
    myString='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='Store,'+store_id+'|'+store_name+'\n'
    myString+='RSM,'+rsm_id+'|'+rsm_name+'\n'
    myString+='FM,'+fm_id+'|'+fm_name+'\n'
    myString+='TR,'+tr_id+'|'+tr_name+'\n\n\n'
    myString+='Zone , RSM ,  InvCount  ,  Total TP  ,TP A  ,  TP B  ,  TPC\n'
    for i in range(len(records)):
        record=records[i]
        category_id=record['category_id']
        amnt=record['amnt']
        if rsm_past!=record['level1_id']:
            cat_str=cat_str+'<fdrd'+str(record['level1_id'])+'>'
        if category_id=='A':
            amnA=str(amnt)
        if category_id=='B':
            amnB=str(amnt)
        if category_id=='C':
            amnC=str(amnt)
        cat_str=cat_str+amnA+','+amnB+','+amnC+'<rd>'
        rsm_past=record['level1_id']
#     return cat_str
#     strShow=''
    pastRsm=''
    ATotal=0
    BTotal=0
    CTotal=0
    Total=0
    for i in range(len(records)):    
        record=records[i]
        spStr='<fdrd'+str(record['level1_id'])+'>'
        #=cat_str
        rsmStr=cat_str.split(spStr)[1].split('<fdrd')[0]
        rsmStrList=rsmStr.split('<rd>')
        i=0
        while i < len(rsmStrList)-1:
            amnA='0'
            amnB='0'
            amnC='0'
            catA=rsmStrList[i].split(',')[0]
            catB=rsmStrList[i].split(',')[1]
            catC=rsmStrList[i].split(',')[2]
            i=i+1
        
        ATotal=ATotal+float(catA)
        BTotal=BTotal+float(catB)
        CTotal=CTotal+float(catC)
        Total=float(catA)+float(catB)+float(catC)
    
    
# ===========     
        
        rsm=record['level1_id']
        invCount=0
        if [s for s in rsmList if rsm in s]:
            index_element = rsmList.index(rsm)           
            invCount= invCountList[index_element]
        
        if pastRsm!=record['level1_id']:
            myString+=str(record['level0_id'])+','+str(record['level1_id'])+','+str(invCount)+','+str(Total)+','+str(ATotal)+','+str(BTotal)+','+str(CTotal)+'\n'
#         strShow= strShow+' past:'+str(pastRsm)+' rec:'+str(record['level0_id']) 
        pastRsm= record['level1_id']
#     return strShow
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=RSMSummary.csv'   
    return str(myString)


# ===================================================
def scFm():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    tr_id=str(request.vars.tr_id).strip()
    tr_name=str(request.vars.tr_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

  
    conditionH=''
    if (depot_id!=''):
        conditionH=conditionH+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        conditionH=conditionH+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        conditionH=conditionH+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        conditionH=conditionH+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        conditionH=conditionH+"AND level3_id = '"+str(tr_id)+"'"
    dateRecordsH="SELECT  level2_id, count(DISTINCT  sl) as invcount FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+conditionH+" GROUP BY level2_id ORDER BY level2_id;"
#     return dateRecordsH
    records_head=db.executesql(dateRecordsH,as_dict = True) 
    
    rsmList=[]
    invCountList=[]
    for records_head in records_head:
        rsmList.append(records_head['level2_id'])
        invCountList.append(records_head['invcount'])


    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"

    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        condition=condition+"AND level3_id = '"+str(tr_id)+"'"
   
    dateRecords="SELECT category_id,level1_id ,level2_id, SUM((quantity - return_qty) * actual_tp) as amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY level2_id, category_id ORDER BY level2_id, category_id;"
#     return dateRecords
    records=db.executesql(dateRecords,as_dict = True) 

    cat_str=''
    rsm_past=''
    
    totalAmount=0
    amnt=0
    for i in range(len(records)):
        record=records[i]
        
        category_id=record['category_id']
        amnt=record['amnt']
        if rsm_past!=record['level2_id']:
            cat_str=cat_str+'<fdrd'+str(record['level2_id'])+'>'
            amnA='0'
            amnB='0'
            amnC='0'
        if category_id=='A':
            amnA=str(amnt)
        if category_id=='B':
            amnB=str(amnt)
        if category_id=='C':
            amnC=str(amnt)
        cat_str=cat_str+amnA+','+amnB+','+amnC+'<rd>'
        rsm_past=record['level2_id']
#     return cat_str
    return dict(records=records,rsmList=rsmList,invCountList=invCountList,cat_str=cat_str,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name)

# ========================
def scFmD():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    tr_id=str(request.vars.tr_id).strip()
    tr_name=str(request.vars.tr_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

  
    conditionH=''
    if (depot_id!=''):
        conditionH=conditionH+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        conditionH=conditionH+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        conditionH=conditionH+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        conditionH=conditionH+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        conditionH=conditionH+"AND level3_id = '"+str(tr_id)+"'"
    dateRecordsH="SELECT  level2_id, count(DISTINCT  sl) as invcount FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+conditionH+" GROUP BY level2_id ORDER BY level2_id;"
#     return dateRecordsH
    records_head=db.executesql(dateRecordsH,as_dict = True) 
    
    rsmList=[]
    invCountList=[]
    for records_head in records_head:
        rsmList.append(records_head['level2_id'])
        invCountList.append(records_head['invcount'])


    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"

    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        condition=condition+"AND level3_id = '"+str(tr_id)+"'"
   
    dateRecords="SELECT category_id,level1_id ,level2_id, SUM((quantity - return_qty) * actual_tp) as amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY level2_id, category_id ORDER BY level2_id, category_id;"
#     return dateRecords
    records=db.executesql(dateRecords,as_dict = True) 

    cat_str=''
    rsm_past=''
    
    totalAmount=0
    amnt=0
    for i in range(len(records)):
        record=records[i]
        
        category_id=record['category_id']
        amnt=record['amnt']
        if rsm_past!=record['level2_id']:
            cat_str=cat_str+'<fdrd'+str(record['level2_id'])+'>'
            amnA='0'
            amnB='0'
            amnC='0'
        if category_id=='A':
            amnA=str(amnt)
        if category_id=='B':
            amnB=str(amnt)
        if category_id=='C':
            amnC=str(amnt)
        cat_str=cat_str+amnA+','+amnB+','+amnC+'<rd>'
        rsm_past=record['level2_id']
    
    
    strShow=''
    pastRsm=''
    ATotal=0
    BTotal=0
    CTotal=0
    Total=0
    rsm_past=''
    amnA='0'
    amnB='0'
    amnC='0'
    totalAmount=0
    amnt=0
    myString='Date Range,'+date_from+'to'+date_to+'\n'
    myString='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='Store,'+store_id+'|'+store_name+'\n\n\n'
    myString+='RSM , FM,  InvCount  ,  Total TP  ,TP A  ,  TP B  ,  TPC\n'
    for i in range(len(records)):    
        record=records[i]
        spStr='<fdrd'+str(record['level2_id'])+'>'
        rsmStr=cat_str.split(spStr)[1].split('<fdrd')[0]
        rsmStrList=rsmStr.split('<rd>')
        i=0
        while i < len(rsmStrList)-1:
            catA=rsmStrList[i].split(',')[0]
            catB=rsmStrList[i].split(',')[1]
            catC=rsmStrList[i].split(',')[2]
            i=i+1
        
        ATotal=ATotal+float(catA)
        BTotal=BTotal+float(catB)
        CTotal=CTotal+float(catC)
        Total=float(catA)+float(catB)+float(catC)

# ===========     
        rsm=record['level2_id']
        invCount=0
        if [s for s in rsmList if rsm in s]:
            index_element = rsmList.index(rsm)           
            invCount= invCountList[index_element]
        
        if pastRsm != record['level2_id']:
            myString+=str(record['level1_id'])+','+str(record['level2_id'])+','+str(invCount)+','+str(Total)+','+str(ATotal)+','+str(BTotal)+','+str(CTotal)+'\n'
        strShow = strShow+' past:'+str(pastRsm)+' rec:'+str(record['level2_id'])
        pastRsm = record['level2_id']
         
#         return strShow
        
#     return strShow
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=FMSummary.csv'   
    return str(myString)

# ==========================================================
def scTr():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    tr_id=str(request.vars.tr_id).strip()
    tr_name=str(request.vars.tr_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

  
    conditionH=''
    if (depot_id!=''):
        conditionH=conditionH+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        conditionH=conditionH+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        conditionH=conditionH+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        conditionH=conditionH+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        conditionH=conditionH+"AND level3_id = '"+str(tr_id)+"'"
    dateRecordsH="SELECT  level3_id, count(DISTINCT  sl) as invcount FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+conditionH+" GROUP BY level3_id ORDER BY level3_id;"
#     return dateRecordsH
    records_head=db.executesql(dateRecordsH,as_dict = True) 
    rsmList=[]
    invCountList=[]
    for records_head in records_head:
        rsmList.append(records_head['level3_id'])
        invCountList.append(records_head['invcount'])


    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        condition=condition+"AND level3_id = '"+str(tr_id)+"'"
    
    dateRecords="SELECT category_id, level1_id,level2_id, level3_id, SUM((quantity - return_qty) * actual_tp) as amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY level3_id, category_id ORDER BY level3_id, category_id;"
    records=db.executesql(dateRecords,as_dict = True) 

    cat_str=''
    rsm_past=''
    
    totalAmount=0
    amnt=0
    for i in range(len(records)):
        record=records[i]
        category_id=record['category_id']
        amnt=record['amnt']
        if rsm_past!=record['level3_id']:
            cat_str=cat_str+'<fdrd'+str(record['level3_id'])+'>'
            amnA='0'
            amnB='0'
            amnC='0'
        if category_id=='A':
            amnA=str(amnt)
        if category_id=='B':
            amnB=str(amnt)
        if category_id=='C':
            amnC=str(amnt)
        cat_str=cat_str+amnA+','+amnB+','+amnC+'<rd>'
        rsm_past=record['level3_id']
#     return cat_str
    return dict(records=records,rsmList=rsmList,invCountList=invCountList,cat_str=cat_str,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name)


def scTrD():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    tr_id=str(request.vars.tr_id).strip()
    tr_name=str(request.vars.tr_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

  
    conditionH=''
    if (depot_id!=''):
        conditionH=conditionH+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        conditionH=conditionH+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        conditionH=conditionH+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        conditionH=conditionH+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        conditionH=conditionH+"AND level3_id = '"+str(tr_id)+"'"
    dateRecordsH="SELECT  level3_id, count(DISTINCT  sl) as invcount FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+conditionH+" GROUP BY level3_id ORDER BY level3_id;"
#     return dateRecordsH
    records_head=db.executesql(dateRecordsH,as_dict = True) 
    rsmList=[]
    invCountList=[]
    for records_head in records_head:
        rsmList.append(records_head['level3_id'])
        invCountList.append(records_head['invcount'])


    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        condition=condition+"AND level3_id = '"+str(tr_id)+"'"
    
    dateRecords="SELECT category_id, level1_id,level2_id, level3_id, SUM((quantity - return_qty) * actual_tp) as amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY level3_id, category_id ORDER BY level3_id, category_id;"
    records=db.executesql(dateRecords,as_dict = True) 

    cat_str=''
    rsm_past=''
    
    totalAmount=0
    amnt=0
    for i in range(len(records)):
        record=records[i]
        category_id=record['category_id']
        amnt=record['amnt']
        if rsm_past!=record['level3_id']:
            cat_str=cat_str+'<fdrd'+str(record['level3_id'])+'>'
            amnA='0'
            amnB='0'
            amnC='0'
        if category_id=='A':
            amnA=str(amnt)
        if category_id=='B':
            amnB=str(amnt)
        if category_id=='C':
            amnC=str(amnt)
        cat_str=cat_str+amnA+','+amnB+','+amnC+'<rd>'
        rsm_past=record['level3_id']

    
    
    
    strShow=''
    pastRsm=''
    ATotal=0
    BTotal=0
    CTotal=0
    Total=0
    rsm_past=''
    amnA='0'
    amnB='0'
    amnC='0'
    totalAmount=0
    amnt=0
    myString='Date Range,'+date_from+'to'+date_to+'\n'
    myString='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='Store,'+store_id+'|'+store_name+'\n\n\n'
    myString+='RSM , FM,TR,  InvCount  ,  Total TP  ,TP A  ,  TP B  ,  TPC\n'
    for i in range(len(records)):    
        record=records[i]
        spStr='<fdrd'+str(record['level3_id'])+'>'
        rsmStr=cat_str.split(spStr)[1].split('<fdrd')[0]
        rsmStrList=rsmStr.split('<rd>')
        i=0
        while i < len(rsmStrList)-1:
            catA=rsmStrList[i].split(',')[0]
            catB=rsmStrList[i].split(',')[1]
            catC=rsmStrList[i].split(',')[2]
            i=i+1
        
        ATotal=ATotal+float(catA)
        BTotal=BTotal+float(catB)
        CTotal=CTotal+float(catC)
        Total=float(catA)+float(catB)+float(catC)

# ===========     
        rsm=record['level3_id']
        invCount=0
        if [s for s in rsmList if rsm in s]:
            index_element = rsmList.index(rsm)           
            invCount= invCountList[index_element]
        
        if pastRsm != record['level3_id']:
            myString+=str(record['level1_id'])+','+str(record['level2_id'])+','+str(record['level3_id'])+','+str(invCount)+','+str(Total)+','+str(ATotal)+','+str(BTotal)+','+str(CTotal)+'\n'
        strShow = strShow+' past:'+str(pastRsm)+' rec:'+str(record['level2_id'])
        pastRsm = record['level3_id']
         
#         return strShow
        
#     return strShow
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=TRSummary.csv'   
    return str(myString)


# ==============================================
def scTrDetail():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    tr_id=str(request.vars.tr_id).strip()
    tr_name=str(request.vars.tr_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

  
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.quantity>0)
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)      
    if (depot_id!=''):
        qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_depot_stock_balance.store_id==store_id) 
    records=qset.select(db.sm_item.item_id,db.sm_item.name,db.sm_item.category_id,db.sm_depot_stock_balance.quantity.sum(),db.sm_item.price,orderby=db.sm_item.name,groupby=db.sm_item.item_id)
    prodDict={}
    prodList=[]
    itemList=[]
    for record in records:
        item_id= record[db.sm_item.item_id]
        item_name= record[db.sm_item.name]
        category_id = record[db.sm_item.category_id]
        stockBalance = record[db.sm_depot_stock_balance.quantity.sum()]
        TP= record[db.sm_item.price]
        
        prodDict={'item_id':item_id,'item_name':item_name,'category_id':category_id,'stockBalance':stockBalance,'TP':TP}
        prodList.append(prodDict)
        itemList.append(item_id)
        
    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        condition=condition+"AND level3_id = '"+str(tr_id)+"'"

    dateRecords="SELECT item_id,item_name,actual_tp,category_id,level1_id,level2_id ,level3_id, SUM(quantity - return_qty)  as qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY level3_id, category_id,item_id ORDER BY   level3_id,item_id,category_id;"
    records=db.executesql(dateRecords,as_dict = True) 

    return dict(records=records,prodList=prodList,itemList=itemList,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name)
def scTrDetailD():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

  
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.quantity>0)
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)      
    if (depot_id!=''):
        qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_depot_stock_balance.store_id==store_id) 
    records=qset.select(db.sm_item.item_id,db.sm_item.name,db.sm_item.category_id,db.sm_depot_stock_balance.quantity.sum(),db.sm_item.price,orderby=db.sm_item.name,groupby=db.sm_item.item_id)
    prodDict={}
    prodList=[]
    itemList=[]
    for record in records:
        item_id= record[db.sm_item.item_id]
        item_name= record[db.sm_item.name]
        category_id = record[db.sm_item.category_id]
        stockBalance = record[db.sm_depot_stock_balance.quantity.sum()]
        TP= record[db.sm_item.price]
        
        prodDict={'item_id':item_id,'item_name':item_name,'category_id':category_id,'stockBalance':stockBalance,'TP':TP}
        prodList.append(prodDict)
        itemList.append(item_id)
        
    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"

    dateRecords="SELECT item_id,item_name,actual_tp,category_id,level1_id,level2_id ,level3_id, SUM(quantity - return_qty)  as qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY level3_id, category_id,item_id ORDER BY   level3_id,item_id,category_id;"
    records=db.executesql(dateRecords,as_dict = True) 

    return dict(records=records,prodList=prodList,itemList=itemList,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name)

# ==============================================
def scFmDetail():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    tr_id=str(request.vars.tr_id).strip()
    tr_name=str(request.vars.tr_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

  
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.quantity>0)
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)      
    if (depot_id!=''):
        qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_depot_stock_balance.store_id==store_id) 
    records=qset.select(db.sm_item.item_id,db.sm_item.name,db.sm_item.category_id,db.sm_depot_stock_balance.quantity.sum(),db.sm_item.price,orderby=db.sm_item.name,groupby=db.sm_item.item_id)
    prodDict={}
    prodList=[]
    itemList=[]
    for record in records:
        item_id= record[db.sm_item.item_id]
        item_name= record[db.sm_item.name]
        category_id = record[db.sm_item.category_id]
        stockBalance = record[db.sm_depot_stock_balance.quantity.sum()]
        TP= record[db.sm_item.price]
        
        prodDict={'item_id':item_id,'item_name':item_name,'category_id':category_id,'stockBalance':stockBalance,'TP':TP}
        prodList.append(prodDict)
        itemList.append(item_id)
        
    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        condition=condition+"AND level3_id = '"+str(tr_id)+"'"
        

    dateRecords="SELECT item_id,item_name,actual_tp,category_id,level1_id,level2_id ,level3_id, SUM(quantity - return_qty)  as qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY level2_id, category_id,item_id ORDER BY   level2_id,item_id,category_id;"
    records=db.executesql(dateRecords,as_dict = True) 

    return dict(records=records,prodList=prodList,itemList=itemList,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name)

def scRsmDetail():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    tr_id=str(request.vars.tr_id).strip()
    tr_name=str(request.vars.tr_name).strip()
    
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

  
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.quantity>0)
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)      
    if (depot_id!=''):
        qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_depot_stock_balance.store_id==store_id) 
    records=qset.select(db.sm_item.item_id,db.sm_item.name,db.sm_item.category_id,db.sm_depot_stock_balance.quantity.sum(),db.sm_item.price,orderby=db.sm_item.name,groupby=db.sm_item.item_id)
    prodDict={}
    prodList=[]
    itemList=[]
    for record in records:
        item_id= record[db.sm_item.item_id]
        item_name= record[db.sm_item.name]
        category_id = record[db.sm_item.category_id]
        stockBalance = record[db.sm_depot_stock_balance.quantity.sum()]
        TP= record[db.sm_item.price]
        
        prodDict={'item_id':item_id,'item_name':item_name,'category_id':category_id,'stockBalance':stockBalance,'TP':TP}
        prodList.append(prodDict)
        itemList.append(item_id)
        
    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        condition=condition+"AND level3_id = '"+str(tr_id)+"'"

    dateRecords="SELECT item_id,item_name,actual_tp,category_id,level1_id,level2_id ,level3_id, SUM(quantity - return_qty)  as qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY level1_id, category_id,item_id ORDER BY   level1_id,item_id,category_id;"
    records=db.executesql(dateRecords,as_dict = True) 

    return dict(records=records,prodList=prodList,itemList=itemList,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name)


def scRsmDetailD():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

  
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.quantity>0)
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)      
    if (depot_id!=''):
        qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_depot_stock_balance.store_id==store_id) 
    records=qset.select(db.sm_item.item_id,db.sm_item.name,db.sm_item.category_id,db.sm_depot_stock_balance.quantity.sum(),db.sm_item.price,orderby=db.sm_item.name,groupby=db.sm_item.item_id)
    prodDict={}
    prodList=[]
    itemList=[]
    for record in records:
        item_id= record[db.sm_item.item_id]
        item_name= record[db.sm_item.name]
        category_id = record[db.sm_item.category_id]
        stockBalance = record[db.sm_depot_stock_balance.quantity.sum()]
        TP= record[db.sm_item.price]
        
        prodDict={'item_id':item_id,'item_name':item_name,'category_id':category_id,'stockBalance':stockBalance,'TP':TP}
        prodList.append(prodDict)
        itemList.append(item_id)
        
    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"

    dateRecords="SELECT item_id,item_name,actual_tp,category_id,level1_id,level2_id ,level3_id, SUM(quantity - return_qty)  as qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY level1_id, category_id,item_id ORDER BY   level1_id,item_id,category_id;"
    records=db.executesql(dateRecords,as_dict = True) 

    return dict(records=records,prodList=prodList,itemList=itemList,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name)


def scMarketDetail():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    tr_id=str(request.vars.tr_id).strip()
    tr_name=str(request.vars.tr_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

  
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.quantity>0)
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)      
    if (depot_id!=''):
        qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_depot_stock_balance.store_id==store_id) 
    records=qset.select(db.sm_item.item_id,db.sm_item.name,db.sm_item.category_id,db.sm_depot_stock_balance.quantity.sum(),db.sm_item.price,orderby=db.sm_item.name,groupby=db.sm_item.item_id)
    prodDict={}
    prodList=[]
    itemList=[]
    for record in records:
        item_id= record[db.sm_item.item_id]
        item_name= record[db.sm_item.name]
        category_id = record[db.sm_item.category_id]
        stockBalance = record[db.sm_depot_stock_balance.quantity.sum()]
        TP= record[db.sm_item.price]
        
        prodDict={'item_id':item_id,'item_name':item_name,'category_id':category_id,'stockBalance':stockBalance,'TP':TP}
        prodList.append(prodDict)
        itemList.append(item_id)
        
    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        condition=condition+"AND level3_id = '"+str(tr_id)+"'"

    dateRecords="SELECT item_id,item_name,actual_tp,category_id,level1_id,level2_id ,level3_id,market_id,market_name, SUM(quantity - return_qty)  as qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY market_id, category_id,item_id ORDER BY   market_id,item_id,category_id;"
    records=db.executesql(dateRecords,as_dict = True) 

    return dict(records=records,prodList=prodList,itemList=itemList,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name)