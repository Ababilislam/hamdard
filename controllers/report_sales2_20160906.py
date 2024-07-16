import calendar

def sub_months(sourcedate, months):    
    month = sourcedate.month - 1 - months
    year = sourcedate.year + month / 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)

def home():
    task_id='rm_analysis_view'
    access_permission=check_role(task_id)
    if (access_permission==False ):
        session.flash='Access is Denied'
        redirect (URL('default','home'))
        
    response.title='Report:Sales-2'
    
    c_id=session.cid
    
    search_form =SQLFORM(db.sm_search_date)
    
    #-------------Billal
    btn_inv_ret_details=request.vars.btn_inv_ret_details
    btn_inv_ret_details_D=request.vars.btn_inv_ret_details_D
    btn_inv_ret_itemwise=request.vars.btn_inv_ret_itemwise
    btn_inv_ret_itemwise_D=request.vars.btn_inv_ret_itemwise_D
    btn_inv_ret_checking=request.vars.btn_inv_ret_checking
    btn_inv_ret_checking_D=request.vars.btn_inv_ret_checking_D
    btn_return_note_preview=request.vars.btn_return_note_preview
    
    btn_invoice_exclusive_bonus=request.vars.btn_invoice_exclusive_bonus
    
    btn_discount_typewise_sale=request.vars.btn_discount_typewise_sale
    btn_discount_typewise_sale_D=request.vars.btn_discount_typewise_sale_D
    btn_discount_typewise_sale_ad=request.vars.btn_discount_typewise_sale_ad
    btn_discount_typewise_sale_with_tp=request.vars.btn_discount_typewise_sale_with_tp
    
    btn_discount_typewise_sale_with_value=request.vars.btn_discount_typewise_sale_with_value
    
    btn_customer_sub_cat_wise_sale_statement=request.vars.btn_customer_sub_cat_wise_sale_statement
    btn_covered_customer_list=request.vars.btn_covered_customer_list
    btn_accounting_period_invoice_wise=request.vars.btn_accounting_period_invoice_wise
    btn_customer_type_wise_sales=request.vars.btn_customer_type_wise_sales
    
    btn_sales_vat_discount_reconciliation=request.vars.btn_sales_vat_discount_reconciliation
    btn_ar_reconciliation=request.vars.btn_ar_reconciliation
    
    #End Billal
    
    #--------------- Billal
    #     Billal
    if (btn_inv_ret_details or btn_inv_ret_details_D or btn_inv_ret_itemwise or btn_inv_ret_itemwise_D or btn_inv_ret_checking or btn_inv_ret_checking_D or btn_discount_typewise_sale or btn_discount_typewise_sale_D or btn_discount_typewise_sale_ad or btn_discount_typewise_sale_with_value or btn_discount_typewise_sale_with_tp or btn_accounting_period_invoice_wise or btn_customer_type_wise_sales or btn_return_note_preview or btn_invoice_exclusive_bonus):
        date_from=request.vars.from_dt_2
        date_to=request.vars.to_dt_2
        
        depot=str(request.vars.sales_depot_id_sales2)
        store=str(request.vars.store_id_sales2)
        
        customer=str(request.vars.customer_id_sales2)
        customerCat=str(request.vars.customer_category2)
        customer_market=str(request.vars.customer_market2)
        dman=str(request.vars.dman_id_sales2)
        teritory=str(request.vars.t_id_sales2)
        mso=str(request.vars.mso_id_sales2)
        discount_type=str(request.vars.discount_type)
            
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
            if dateDiff>92:
                response.flash="Maximum 92 days allowed between Date Range"
            else:
                if (depot=='' or store==''):
                    session.flash="Required Branch and Store"
                    redirect(URL(c='report_sales2',f='home'))
                else:                 
                    if (depot!=''): 
                        depot_id=depot.split('|')[0].upper().strip()                        
                    else:
                        depot_id=depot
                        
                    user_depot_address=''
                    if session.user_type!='Depot': 
                        depotRows = db((db.sm_depot.cid == session.cid) & (db.sm_depot.depot_id == depot_id)).select(db.sm_depot.name,db.sm_depot.depot_category,db.sm_depot.field1, limitby=(0, 1))
                        if depotRows:
                            user_depot_address=depotRows[0].field1         
                            session.user_depot_address=user_depot_address
                            
                    if (store!=''): 
                        store_id=store.split('|')[0].upper().strip()                        
                    else:
                        store_id=store
                    
                    if (customer!=''): 
                        customer_id=customer.split('|')[0].upper().strip()                        
                    else:
                        customer_id=customer
                    
                    if (customerCat!=''): 
                        customerCat_id=customerCat.split('|')[0].upper().strip()                        
                    else:
                        customerCat_id=customerCat
                    
                    if (dman!=''): 
                        dman_id=dman.split('|')[0].upper().strip()                        
                    else:
                        dman_id=dman
                    
                    if (teritory!=''): 
                        teritory_id=teritory.split('|')[0].upper().strip()                        
                    else:
                        teritory_id=teritory
                    
                    if (customer_market!=''): 
                        market_id=customer_market.split('|')[0].upper().strip()                        
                    else:
                        market_id=customer_market
                    
                    if (mso!=''): 
                        mso_id=mso.split('|')[0].upper().strip()                        
                    else:
                        mso_id=mso
                    
                    
                    # report function
                    if btn_inv_ret_details:                        
                        redirect (URL('invoice_return_details',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,store_id=store_id,customer_id=customer_id,dman_id=dman_id,teritory_id=teritory_id,market_id=market_id,mso_id=mso_id)))
                        
                    elif btn_inv_ret_itemwise:
                        redirect (URL('invoice_return_itemwise',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,store_id=store_id,customer_id=customer_id,dman_id=dman_id,teritory_id=teritory_id,market_id=market_id,mso_id=mso_id)))
                        
                    elif btn_inv_ret_checking:
                        redirect (URL('invoice_return_checking',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,store_id=store_id,customer_id=customer_id,dman_id=dman_id,teritory_id=teritory_id,market_id=market_id,mso_id=mso_id)))
                        
                    elif btn_return_note_preview:
                        redirect (URL('return_note_preview',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,store_id=store_id,customer_id=customer_id,dman_id=dman_id,teritory_id=teritory_id,market_id=market_id,mso_id=mso_id)))
                        
                    elif btn_discount_typewise_sale:
                        redirect (URL('discount_type_wise_sales',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,store_id=store_id,customer_id=customer_id,dman_id=dman_id,teritory_id=teritory_id,market_id=market_id,mso_id=mso_id)))
                        
                    elif btn_discount_typewise_sale_ad:
                        redirect (URL('discount_type_wise_sales_ad',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,store_id=store_id,customer_id=customer_id,dman_id=dman_id,teritory_id=teritory_id,market_id=market_id,mso_id=mso_id)))
                        
                    elif btn_discount_typewise_sale_with_tp:
                        redirect (URL('discount_type_wise_sales_with_tp',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,store_id=store_id,customer_id=customer_id,dman_id=dman_id,teritory_id=teritory_id,market_id=market_id,mso_id=mso_id,discount_type=discount_type)))
                        
                    elif btn_discount_typewise_sale_with_value:
                        redirect (URL('discount_type_wise_sales_with_value',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,store_id=store_id,customer_id=customer_id,dman_id=dman_id,teritory_id=teritory_id,market_id=market_id,mso_id=mso_id)))
                        
                    elif btn_invoice_exclusive_bonus:
                        redirect (URL('invoice_exclusive_bonus',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,store_id=store_id,customer_id=customer_id,dman_id=dman_id,teritory_id=teritory_id,market_id=market_id,mso_id=mso_id)))
                        
                        
                    elif btn_customer_type_wise_sales:
                        redirect (URL('customer_type_wise_sales',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,store_id=store_id,customer_id=customer_id,dman_id=dman_id,teritory_id=teritory_id,market_id=market_id,mso_id=mso_id)))
                        
                    elif btn_accounting_period_invoice_wise:
                        redirect (URL('accounting_period_invoice_wise',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,store_id=store_id,customer_id=customer_id,dman_id=dman_id,teritory_id=teritory_id,market_id=market_id,mso_id=mso_id)))
                    
    elif (btn_sales_vat_discount_reconciliation or btn_ar_reconciliation):
        date_from=request.vars.from_dt_2
        date_to=request.vars.to_dt_2
        
        depot=str(request.vars.sales_depot_id_sales2)
        store=str(request.vars.store_id_sales2)
                        
        dateFlag=True
        try:
            #from_dt2=datetime.datetime.strptime(str(date_from),'%Y-%m-%d')
            to_dt2=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
            
            #if from_dt2>to_dt2:
                #dateFlag=False
        except:
            dateFlag=False
        
        if dateFlag==False:
            response.flash="Invalid To Date"
        else:
            if (depot==''):
                session.flash="Required Branch"
                redirect(URL(c='report_sales2',f='home'))
            else:
                 
                if (depot!=''): 
                    depot_id=depot.split('|')[0].upper().strip()                        
                else:
                    depot_id=depot
                
                  
                user_depot_address=''
                if session.user_type!='Depot': 
                    depotRows = db((db.sm_depot.cid == session.cid) & (db.sm_depot.depot_id == depot_id)).select(db.sm_depot.name,db.sm_depot.depot_category,db.sm_depot.field1, limitby=(0, 1))
                    if depotRows:
                        user_depot_address=depotRows[0].field1         
                        session.user_depot_address=user_depot_address
            
                
                # report function
                if btn_sales_vat_discount_reconciliation:
                    redirect (URL('sales_vat_discount_reconciliation',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id)))
                    
                elif btn_ar_reconciliation:
                    redirect (URL('ar_reconciliation',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id)))
                    
    elif (btn_customer_sub_cat_wise_sale_statement or btn_covered_customer_list):
        date_from=request.vars.from_dt_2
        date_to=request.vars.to_dt_2
        
        depot=str(request.vars.sales_depot_id_sales2)
        store=str(request.vars.store_id_sales2)
        
        customerSubCat=str(request.vars.cust_sub_cat_sales2)
        product=str(request.vars.product_id_sales2)
        
        mso=str(request.vars.mso_id_sales2)
        level1=str(request.vars.level1_sales2)
        level2=str(request.vars.level2_sales2)
        
        dateFlag=True
        try:
            from_dt2=datetime.datetime.strptime(str(date_from),'%Y-%m-%d')
            to_dt2=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
            
            if from_dt2=='' or to_dt2=='':
                dateFlag=False
            else:
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
                if ((depot=='') | (store=='')):
                    response.flash="Required Branch and Store"                    
                else:
                    
                    if (depot!=''): 
                        depot_id=depot.split('|')[0].upper().strip()                        
                    else:
                        depot_id=depot
                    
                      
                    user_depot_address=''
                    if session.user_type!='Depot': 
                        depotRows = db((db.sm_depot.cid == session.cid) & (db.sm_depot.depot_id == depot_id)).select(db.sm_depot.name,db.sm_depot.depot_category,db.sm_depot.field1, limitby=(0, 1))
                        if depotRows:
                            user_depot_address=depotRows[0].field1         
                            session.user_depot_address=user_depot_address
                
                    
                    if (store!=''): 
                        store_id=store.split('|')[0].upper().strip()                        
                    else:
                        store_id=store
                    
                    if (product!=''): 
                        product_id=product.split('|')[0].upper().strip()                        
                    else:
                        product_id=product
                    
                    if (mso!=''): 
                        mso_id=mso.split('|')[0].upper().strip()                        
                    else:
                        mso_id=mso
                        
                    if (level1!=''): 
                        level1_id=level1.split('|')[0].upper().strip()                        
                    else:
                        level1_id=level1
                        
                    if (level2!=''): 
                        level2_id=level2.split('|')[0].upper().strip()                        
                    else:
                        level2_id=level2
                        
                    # report function
                    if btn_customer_sub_cat_wise_sale_statement:
                        if customerSubCat=='' or customerSubCat=='None':
                            response.flash="Required Customer Sub-Category for report 27"
                        else:
                            redirect (URL('customer_sub_cat_wise_sales',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,store_id=store_id,customerSubCat=customerSubCat,product_id=product_id)))
                    
                    elif btn_covered_customer_list:
                        redirect (URL('covered_customer_list',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,store_id=store_id,customerSubCat=customerSubCat,product_id=product_id,mso_id=mso_id,level1_id=level1_id,level2_id=level2_id)))
                    
    #----------End Billal
    
    #-------------------
    custSubCatRows=db((db.sm_category_type.cid == session.cid)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')).select(db.sm_category_type.cat_type_id,db.sm_category_type.cat_type_name,orderby=db.sm_category_type.cat_type_name)
    
    return dict(search_form=search_form,custSubCatRows=custSubCatRows)
    

#===================================================Sales 2 Billal

def invoice_return_details():
    c_id=session.cid
    
    response.title='30.1 Invoice and Return Details'
    
    fromDate=request.vars.date_from
    toDate=request.vars.date_to
    
    depot_id=str(request.vars.depot_id).strip()
    store_id=str(request.vars.store_id).strip()    
    customer_id=str(request.vars.customer_id).strip()
    #customerCat_id=str(request.vars.customerCat_id).strip()
    dman_id=str(request.vars.dman_id).strip()    
    territory_id=str(request.vars.teritory_id).strip()  
    market_id=str(request.vars.market_id).strip()
    mso_id=str(request.vars.mso_id).strip()
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
    
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customer_id)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
        
    #customerCatName=''
    #clientCatRow=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customerCat_id)).select(db.sm_category_type.cat_type_name,limitby=(0,1))
    #if clientCatRow:
        #customerCatName=clientCatRow[0].cat_type_name
    
    delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==dman_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        delivery_man_name=dpRow[0].name
        
    territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        territory_name=levelRow[0].level_name
        
    market_name=''
    marketRow=db((db.sm_depot_market.cid==c_id) & (db.sm_depot_market.depot_id==depot_id) & (db.sm_depot_market.market_id==market_id)).select(db.sm_depot_market.market_name,limitby=(0,1))
    if marketRow:
        market_name=marketRow[0].market_name
        
    mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        mso_name=repRow[0].name
    
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
    
    condStr=" AND (round((sm_invoice_head.return_tp+sm_invoice_head.return_vat-sm_invoice_head.return_discount),2)!=0)"
    
    if customer_id!='':
        condStr+=" AND (sm_invoice_head.client_id='"+customer_id+"')"        
    if dman_id!='':
        condStr+=" AND (sm_invoice_head.d_man_id='"+dman_id+"')"        
    if territory_id!='':
        condStr+=" AND (sm_invoice_head.area_id='"+territory_id+"')"      
    if market_id!='':
        condStr+=" AND (sm_invoice_head.market_id='"+market_id+"')"      
    if mso_id!='':
        condStr+=" AND (sm_invoice_head.rep_id='"+mso_id+"')"        
        
    if startDt!='' and endDt!='': 
        dateRecords="SELECT sm_invoice_head.depot_id as depot_id,sm_invoice_head.invoice_date as invoice_date,sm_invoice_head.sl as invSl,sm_invoice_head.client_id as client_id,sm_invoice_head.client_name as client_name,sm_invoice_head.actual_total_tp as actualTpAmt,sm_invoice_head.vat_total_amount as vatTotalAmt,sm_invoice_head.discount as discAmt,sm_invoice_head.sp_discount as spDiscAmt,sm_invoice_head.return_tp as retTpAmt,sm_invoice_head.return_vat as retVatAmt,sm_invoice_head.return_discount as retDiscAmt,sm_invoice_head.return_sp_discount as retSpDiscAmt FROM sm_invoice_head WHERE ((sm_invoice_head.cid = '"+c_id+"') AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.store_id='"+store_id+"') AND ((sm_invoice_head.invoice_date >= '"+str(startDt)+"') AND (sm_invoice_head.invoice_date <= '"+str(endDt)+"')) AND (sm_invoice_head.status='Invoiced') "+str(condStr)+") ORDER BY sm_invoice_head.sl"
    else:
        dateRecords=''
        response.flash='Required Date From and Date To'
        
    recordList=db.executesql(dateRecords,as_dict = True)
    
    invList=[]
    invocieCount=0
    for i in range(len(recordList)):
        dictData=recordList[i]
        invList.append(dictData['invSl'])
        invocieCount+=1
        
    retRows=db((db.sm_return_head.cid==c_id)&(db.sm_return_head.depot_id==depot_id)&(db.sm_return_head.invoice_sl.belongs(invList))&(db.sm_return_head.status=='Returned')).select(db.sm_return_head.depot_id,db.sm_return_head.invoice_sl,db.sm_return_head.sl,db.sm_return_head.return_date,orderby=db.sm_return_head.sl)
    
    retRowsDate=db((db.sm_return_head.cid==c_id)&(db.sm_return_head.depot_id==depot_id)&(db.sm_return_head.invoice_sl.belongs(invList))&(db.sm_return_head.status=='Returned')).select(db.sm_return_head.depot_id,db.sm_return_head.return_date.min(),db.sm_return_head.return_date.max(),groupby=db.sm_return_head.depot_id)
    
    returnDateFrom=''
    returnDateTo=''
    if retRowsDate:
        returnDateFrom=retRowsDate[0][db.sm_return_head.return_date.min()]
        returnDateTo=retRowsDate[0][db.sm_return_head.return_date.max()]
        
    return dict(recordList=recordList,invocieCount=invocieCount,returnDateFrom=returnDateFrom,returnDateTo=returnDateTo,retRows=retRows,date_from=startDt,date_to=endDt,depot_id=depot_id,depotName=depot_name,store_id=store_id,storeName=store_name,dman_id=dman_id,delivery_man_name=delivery_man_name,territory_id=territory_id,territory_name=territory_name,mso_id=mso_id,mso_name=mso_name,customer_id=customer_id,customerName=customerName,market_id=market_id,market_name=market_name,page=page,items_per_page=items_per_page)    

def invoice_return_details_download():
    c_id=session.cid
    
    response.title='30.1 Invoice and Return Details'
    
    fromDate=request.vars.date_from
    toDate=request.vars.date_to
    
    depot_id=str(request.vars.depot_id).strip()
    store_id=str(request.vars.store_id).strip()    
    customer_id=str(request.vars.customer_id).strip()
    #customerCat_id=str(request.vars.customerCat_id).strip()
    dman_id=str(request.vars.dman_id).strip()    
    territory_id=str(request.vars.territory_id).strip()  
    market_id=str(request.vars.market_id).strip()
    mso_id=str(request.vars.mso_id).strip()
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
    
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customer_id)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
        
    #customerCatName=''
    #clientCatRow=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customerCat_id)).select(db.sm_category_type.cat_type_name,limitby=(0,1))
    #if clientCatRow:
        #customerCatName=clientCatRow[0].cat_type_name
    
    delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==dman_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        delivery_man_name=dpRow[0].name
        
    territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        territory_name=levelRow[0].level_name
        
    market_name=''
    marketRow=db((db.sm_depot_market.cid==c_id) & (db.sm_depot_market.depot_id==depot_id) & (db.sm_depot_market.market_id==market_id)).select(db.sm_depot_market.market_name,limitby=(0,1))
    if marketRow:
        market_name=marketRow[0].market_name
        
    mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        mso_name=repRow[0].name
    
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
    
    condStr=" AND (round((sm_invoice_head.return_tp+sm_invoice_head.return_vat-sm_invoice_head.return_discount),2)!=0)"
    
    if customer_id!='':
        condStr+=" AND (sm_invoice_head.client_id='"+customer_id+"')"        
    if dman_id!='':
        condStr+=" AND (sm_invoice_head.d_man_id='"+dman_id+"')"        
    if territory_id!='':
        condStr+=" AND (sm_invoice_head.area_id='"+territory_id+"')"      
    if market_id!='':
        condStr+=" AND (sm_invoice_head.market_id='"+market_id+"')"      
    if mso_id!='':
        condStr+=" AND (sm_invoice_head.rep_id='"+mso_id+"')"        
        
    if startDt!='' and endDt!='': 
        dateRecords="SELECT sm_invoice_head.depot_id as depot_id,sm_invoice_head.invoice_date as invoice_date,sm_invoice_head.sl as invSl,sm_invoice_head.client_id as client_id,sm_invoice_head.client_name as client_name,sm_invoice_head.actual_total_tp as actualTpAmt,sm_invoice_head.vat_total_amount as vatTotalAmt,sm_invoice_head.discount as discAmt,sm_invoice_head.sp_discount as spDiscAmt,sm_invoice_head.return_tp as retTpAmt,sm_invoice_head.return_vat as retVatAmt,sm_invoice_head.return_discount as retDiscAmt,sm_invoice_head.return_sp_discount as retSpDiscAmt FROM sm_invoice_head WHERE ((sm_invoice_head.cid = '"+c_id+"') AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.store_id='"+store_id+"') AND ((sm_invoice_head.invoice_date >= '"+str(startDt)+"') AND (sm_invoice_head.invoice_date <= '"+str(endDt)+"')) AND (sm_invoice_head.status='Invoiced') "+str(condStr)+") ORDER BY sm_invoice_head.sl"
    else:
        dateRecords=''
        response.flash='Required Date From and Date To'
        
    recordList=db.executesql(dateRecords,as_dict = True)
    
    invList=[]
    invocieCount=0
    for i in range(len(recordList)):
        dictData=recordList[i]
        invList.append(dictData['invSl'])
        invocieCount+=1
        
    retRows=db((db.sm_return_head.cid==c_id)&(db.sm_return_head.depot_id==depot_id)&(db.sm_return_head.invoice_sl.belongs(invList))&(db.sm_return_head.status=='Returned')).select(db.sm_return_head.depot_id,db.sm_return_head.invoice_sl,db.sm_return_head.sl,db.sm_return_head.return_date,orderby=db.sm_return_head.sl)
    
    retRowsDate=db((db.sm_return_head.cid==c_id)&(db.sm_return_head.depot_id==depot_id)&(db.sm_return_head.invoice_sl.belongs(invList))&(db.sm_return_head.status=='Returned')).select(db.sm_return_head.depot_id,db.sm_return_head.return_date.min(),db.sm_return_head.return_date.max(),groupby=db.sm_return_head.depot_id)
    
    returnDateFrom=''
    returnDateTo=''
    if retRowsDate:
        returnDateFrom=retRowsDate[0][db.sm_return_head.return_date.min()]
        returnDateTo=retRowsDate[0][db.sm_return_head.return_date.max()]
    
    #-------------
    myString='30.1 Invoice and Return Details\n'
    
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depot_name)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(store_name)+'\n'
    myString+='DP ID:,'+str(dman_id)+'\n'
    myString+='DP Name'+','+str(delivery_man_name)+'\n'
    myString+='Territory ID:,'+str(territory_id)+'\n'
    myString+='Territory Name'+','+str(territory_name)+'\n'
    myString+='MSO ID:,'+str(mso_id)+'\n'
    myString+='MSO Name'+','+str(mso_name)+'\n'
    myString+='Market Name'+','+str(market_name)+'\n'
    myString+='Inv. Date From:,'+str(startDt)+'\n'            
    myString+='Inv.To Date:'+','+str(endDt)+'\n'
    myString+='Ret. Date From:,'+str(returnDateFrom)+'\n'            
    myString+='Ret.To Date:'+','+str(returnDateTo)+'\n'
    
    myString+='Document Details,,,,,,Invoice Details,,,,,Return Details'+'\n'
    myString+='Inv.Date,Inv.Number,Cust.ID,Cust.Name,Retn.Date,DR&CR Note,Sales,Discount (Reg+SP),Net Sales,Vat,Sales+Vat,CR/DR Note,Discount (Reg+SP),Net CR/DR Note,Vat,CR/DR Note+Vat'+'\n'
    
    invSaleTotal=0
    invDiscTotal=0
    invNetTotal=0
    invVatTotal=0
    invNetSaleVatTotal=0
    
    retSaleTotal=0
    retDiscTotal=0
    retNetTotal=0
    retVatTotal=0
    retNetSaleVatTotal=0
    
    for i in range(len(recordList)):    
        recData=recordList[i]
        
        #-------------
        retSl=''
        retDate=''
        return_date=''
        for retRow in retRows:
            invoice_sl=retRow.invoice_sl
            if invoice_sl==recData['invSl']:
                sl=str(session.prefix_invoice)+'RET'+str(retRow.depot_id)+'-'+str(retRow.sl)
                return_date=str(retRow.return_date)
                returnDate=str(retRow.return_date.strftime('%d-%b-%Y'))
                
                if retSl=='':
                    retSl=sl
                    retDate=returnDate
                else:
                    retSl+='; '+sl
                    retDate+='; '+returnDate        
                    
        #-----------------        
        invoice_date=recData['invoice_date']                                                            
        invSl=str(session.prefix_invoice)+'INV'+str(recData['depot_id'])+'-'+str(recData['invSl'])
        client_id=recData['client_id']
        client_name=recData['client_name']
        
        invSaleAmt=round(recData['actualTpAmt'],2)        
        invSaleTotal+=invSaleAmt
        
        invDiscAmt=round(recData['discAmt']+recData['spDiscAmt'],2)
        invDiscTotal+=invDiscAmt
        
        invSaleNetAmt=round(invSaleAmt-invDiscAmt,2)
        invNetTotal+=invSaleNetAmt
        
        invVatAmt=round(recData['vatTotalAmt'],2)
        invVatTotal+=invVatAmt
        
        invSaleVatNetAmt=round(invSaleNetAmt+invVatAmt,2)
        invNetSaleVatTotal+=invSaleVatNetAmt
        
        retSaleAmt=round(recData['retTpAmt']+recData['retSpDiscAmt'],2)
        retSaleTotal+=retSaleAmt
        
        retDiscAmt=round(recData['retDiscAmt']+recData['retSpDiscAmt'],2)
        retDiscTotal+=retDiscAmt
        
        retSaleNetAmt=round(retSaleAmt-retDiscAmt,2)
        retNetTotal+=retSaleNetAmt
        
        retVatAmt=round(recData['retVatAmt'],2)
        retVatTotal+=retVatAmt
        
        retSaleVatNetAmt=round(retSaleNetAmt+retVatAmt,2)
        retNetSaleVatTotal+=retSaleVatNetAmt
        
        #------------------------        
        myString+=str(invoice_date)+','+str(invSl)+','+str(client_id)+','+str(client_name)+','+str(retDate)+','+str(retSl)+','+\
        str(invSaleAmt)+','+str(invDiscAmt)+','+str(invSaleNetAmt)+','+str(invVatAmt)+','+str(invSaleVatNetAmt)+','+str(retSaleAmt)+','+str(retDiscAmt)+','+str(retSaleNetAmt)+','+str(retVatAmt)+','+str(retSaleVatNetAmt)+'\n'
        
    myString+=str(invocieCount)+'Invoice(s),Total,,,,,'+str(round(invSaleTotal,2))+','+str(round(invDiscTotal,2))+','+str(round(invNetTotal,2))+','+str(round(invVatTotal,2))+','+str(round(invNetSaleVatTotal,2))+','+str(round(retSaleTotal,2))+','+str(round(retDiscTotal,2))+','+str(round(retNetTotal,2))+','+str(round(retVatTotal,2))+','+str(round(retNetSaleVatTotal,2))+'\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_invoice_return_details.csv'   
    return str(myString)

def invoice_return_itemwise():
    c_id=session.cid
    
    response.title='30.2 Invoice and Return Details Item wise'
    
    fromDate=request.vars.date_from
    toDate=request.vars.date_to
    
    depot_id=str(request.vars.depot_id).strip()
    store_id=str(request.vars.store_id).strip()    
    customer_id=str(request.vars.customer_id).strip()
    #customerCat_id=str(request.vars.customerCat_id).strip()
    dman_id=str(request.vars.dman_id).strip()    
    territory_id=str(request.vars.teritory_id).strip()  
    market_id=str(request.vars.market_id).strip()
    mso_id=str(request.vars.mso_id).strip()
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
    
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customer_id)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
    
    delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==dman_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        delivery_man_name=dpRow[0].name
        
    territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        territory_name=levelRow[0].level_name
        
    market_name=''
    marketRow=db((db.sm_depot_market.cid==c_id) & (db.sm_depot_market.depot_id==depot_id) & (db.sm_depot_market.market_id==market_id)).select(db.sm_depot_market.market_name,limitby=(0,1))
    if marketRow:
        market_name=marketRow[0].market_name
        
    mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        mso_name=repRow[0].name
        
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
    
    condStr=" (sm_invoice.cid = '"+c_id+"') AND (sm_invoice.depot_id='"+depot_id+"') AND (sm_invoice.store_id='"+store_id+"') AND ((sm_invoice.invoice_date >= '"+str(startDt)+"') AND (sm_invoice.invoice_date <= '"+str(endDt)+"')) AND  (sm_invoice.status='Invoiced') AND (sm_invoice.return_qty>0 OR sm_invoice.return_bonus_qty>0)"
    
    if customer_id!='':
        condStr+=" AND (sm_invoice.client_id='"+customer_id+"')"        
    if dman_id!='':
        condStr+=" AND (sm_invoice.d_man_id='"+dman_id+"')"        
    if territory_id!='':
        condStr+=" AND (sm_invoice.area_id='"+territory_id+"')"      
    if market_id!='':
        condStr+=" AND (sm_invoice.market_id='"+market_id+"')"      
    if mso_id!='':
        condStr+=" AND (sm_invoice.rep_id='"+mso_id+"')"        
        
    if startDt!='' and endDt!='': 
        dateRecords="SELECT sm_invoice.item_id as item_id,MAX(sm_invoice.item_name) as item_name,MAX(sm_invoice.item_unit) as item_unit,sm_invoice.actual_tp as actual_tp, SUM(sm_invoice.return_qty) as return_qty, SUM(sm_invoice.return_bonus_qty) as return_bonus_qty FROM sm_invoice WHERE ("+str(condStr)+") GROUP BY sm_invoice.item_id,sm_invoice.actual_tp ORDER BY sm_invoice.item_name asc,sm_invoice.actual_tp desc"
    else:
        dateRecords=''
        response.flash='Required Date From and Date To'
        
    recordList=db.executesql(dateRecords,as_dict = True)
    
    return dict(recordList=recordList,date_from=startDt,date_to=endDt,depot_id=depot_id,depotName=depot_name,store_id=store_id,storeName=store_name,dman_id=dman_id,delivery_man_name=delivery_man_name,territory_id=territory_id,territory_name=territory_name,mso_id=mso_id,mso_name=mso_name,customer_id=customer_id,customerName=customerName,market_id=market_id,market_name=market_name,page=page,items_per_page=items_per_page)    
    
def invoice_return_itemwise_download():
    c_id=session.cid
    
    response.title='30.2 Invoice and Return Details Item wise'
    
    fromDate=request.vars.date_from
    toDate=request.vars.date_to
    
    depot_id=str(request.vars.depot_id).strip()
    store_id=str(request.vars.store_id).strip()    
    customer_id=str(request.vars.customer_id).strip()    
    dman_id=str(request.vars.dman_id).strip()    
    territory_id=str(request.vars.territory_id).strip()  
    market_id=str(request.vars.market_id).strip()
    mso_id=str(request.vars.mso_id).strip()
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
    
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customer_id)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
    
    delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==dman_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        delivery_man_name=dpRow[0].name
        
    territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        territory_name=levelRow[0].level_name
        
    market_name=''
    marketRow=db((db.sm_depot_market.cid==c_id) & (db.sm_depot_market.depot_id==depot_id) & (db.sm_depot_market.market_id==market_id)).select(db.sm_depot_market.market_name,limitby=(0,1))
    if marketRow:
        market_name=marketRow[0].market_name
        
    mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        mso_name=repRow[0].name
    
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
    
    condStr=" (sm_invoice.cid = '"+c_id+"') AND (sm_invoice.depot_id='"+depot_id+"') AND (sm_invoice.store_id='"+store_id+"') AND ((sm_invoice.invoice_date >= '"+str(startDt)+"') AND (sm_invoice.invoice_date <= '"+str(endDt)+"')) AND  (sm_invoice.status='Invoiced') AND (sm_invoice.return_qty>0 OR sm_invoice.return_bonus_qty>0)"
    
    if customer_id!='':
        condStr+=" AND (sm_invoice.client_id='"+customer_id+"')"        
    if dman_id!='':
        condStr+=" AND (sm_invoice.d_man_id='"+dman_id+"')"        
    if territory_id!='':
        condStr+=" AND (sm_invoice.area_id='"+territory_id+"')"      
    if market_id!='':
        condStr+=" AND (sm_invoice.market_id='"+market_id+"')"      
    if mso_id!='':
        condStr+=" AND (sm_invoice.rep_id='"+mso_id+"')"        
    
    
    if startDt!='' and endDt!='': 
        dateRecords="SELECT sm_invoice.item_id as item_id,MAX(sm_invoice.item_name) as item_name,MAX(sm_invoice.item_unit) as item_unit,sm_invoice.actual_tp as actual_tp, SUM(sm_invoice.return_qty) as return_qty, SUM(sm_invoice.return_bonus_qty) as return_bonus_qty FROM sm_invoice WHERE ("+str(condStr)+") GROUP BY sm_invoice.item_id,sm_invoice.actual_tp ORDER BY sm_invoice.item_name asc,sm_invoice.actual_tp desc"
        
    else:
        dateRecords=''
        response.flash='Required Date From and Date To'
        
    recordList=db.executesql(dateRecords,as_dict = True)
    
    #-------------
    myString='30.2 Invoice and Return Details Item wise\n'
    
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depot_name)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(store_name)+'\n'
    myString+='DP ID:,'+str(dman_id)+'\n'
    myString+='DP Name'+','+str(delivery_man_name)+'\n'
    myString+='Territory ID:,'+str(territory_id)+'\n'
    myString+='Territory Name'+','+str(territory_name)+'\n'
    myString+='MSO ID:,'+str(mso_id)+'\n'
    myString+='MSO Name'+','+str(mso_name)+'\n'
    myString+='Market Name'+','+str(market_name)+'\n'
    myString+='Inv. Date From:,'+str(startDt)+'\n'            
    myString+='Inv.To Date:'+','+str(endDt)+'\n'
    
    myString+='SL No.,Product ID,Product Name,Trade Price,Unit,Sale Quantity Return,Bonus Quantity Return,Return TP,Total Quantity Return'+'\n'
    
    rowSl=0
    netRetTotalQty=0
    netRetTp=0   
    for i in range(len(recordList)):
        recData=recordList[i]
    
        rowSl+=1
        
        #-----------------        
        item_id=recData['item_id']
        item_name=recData['item_name']
        actual_tp=recData['actual_tp']
        item_unit=recData['item_unit']
        return_qty=recData['return_qty']
        return_bonus_qty=recData['return_bonus_qty']
        netRetQty=recData['return_qty']+recData['return_bonus_qty']
        
        retTp=float(actual_tp)*int(return_qty)
        netRetTp+=retTp
        
        netRetTotalQty+=netRetQty
        
        #------------------------
        myString+=str(rowSl)+','+str(item_id)+','+str(item_name)+','+str(actual_tp)+','+str(item_unit)+','+str(return_qty)+','+\
        str(return_bonus_qty)+','+str(retTp)+','+str(netRetQty)+'\n'
        
    myString+='Total,,,,,,,'+str(round(netRetTp,2))+','+str(round(netRetTotalQty,2))+'\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_invoice_return_itemWise.csv'   
    return str(myString)
    
def invoice_return_checking():
    c_id=session.cid
    
    response.title='30.3 Invoice wise Return Checking'
    
    fromDate=request.vars.date_from
    toDate=request.vars.date_to
    
    depot_id=str(request.vars.depot_id).strip()
    store_id=str(request.vars.store_id).strip()    
    customer_id=str(request.vars.customer_id).strip()
    #customerCat_id=str(request.vars.customerCat_id).strip()
    dman_id=str(request.vars.dman_id).strip()    
    territory_id=str(request.vars.teritory_id).strip()  
    market_id=str(request.vars.market_id).strip()
    mso_id=str(request.vars.mso_id).strip()
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
    
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customer_id)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
        
    #customerCatName=''
    #clientCatRow=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customerCat_id)).select(db.sm_category_type.cat_type_name,limitby=(0,1))
    #if clientCatRow:
        #customerCatName=clientCatRow[0].cat_type_name
    
    delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==dman_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        delivery_man_name=dpRow[0].name
        
    territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        territory_name=levelRow[0].level_name
        
    market_name=''
    marketRow=db((db.sm_depot_market.cid==c_id) & (db.sm_depot_market.depot_id==depot_id) & (db.sm_depot_market.market_id==market_id)).select(db.sm_depot_market.market_name,limitby=(0,1))
    if marketRow:
        market_name=marketRow[0].market_name
        
    mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        mso_name=repRow[0].name
    
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
    
    condStr=" AND (round((sm_invoice_head.return_tp+sm_invoice_head.return_vat-sm_invoice_head.return_discount),2)!=0)"
    
    if customer_id!='':
        condStr+=" AND (sm_invoice_head.client_id='"+customer_id+"')"        
    if dman_id!='':
        condStr+=" AND (sm_invoice_head.d_man_id='"+dman_id+"')"        
    if territory_id!='':
        condStr+=" AND (sm_invoice_head.area_id='"+territory_id+"')"      
    if market_id!='':
        condStr+=" AND (sm_invoice_head.market_id='"+market_id+"')"      
    if mso_id!='':
        condStr+=" AND (sm_invoice_head.rep_id='"+mso_id+"')"        
        
    if startDt!='' and endDt!='': 
        dateRecords="SELECT sm_invoice_head.depot_id as depot_id,sm_invoice_head.invoice_date as invoice_date,sm_invoice_head.sl as invSl,sm_invoice_head.client_id as client_id,sm_invoice_head.actual_total_tp as actualTpAmt,sm_invoice_head.vat_total_amount as vatTotalAmt,sm_invoice_head.discount as discAmt,sm_invoice_head.sp_discount as spDiscAmt,sm_invoice_head.return_tp as retTpAmt,sm_invoice_head.return_vat as retVatAmt,sm_invoice_head.return_discount as retDiscAmt,sm_invoice_head.return_sp_discount as retSpDiscAmt FROM sm_invoice_head WHERE ((sm_invoice_head.cid = '"+c_id+"') AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.store_id='"+store_id+"') AND ((sm_invoice_head.invoice_date >= '"+str(startDt)+"') AND (sm_invoice_head.invoice_date <= '"+str(endDt)+"')) AND (sm_invoice_head.status='Invoiced') "+str(condStr)+") ORDER BY sm_invoice_head.sl"
    else:
        dateRecords=''
        response.flash='Required Date From and Date To'
        
    recordList=db.executesql(dateRecords,as_dict = True)
    
    invList=[]
    for i in range(len(recordList)):
        dictData=recordList[i]
        invList.append(dictData['invSl'])
        
    retRows=db((db.sm_return_head.cid==c_id)&(db.sm_return_head.depot_id==depot_id)&(db.sm_return_head.invoice_sl.belongs(invList))&(db.sm_return_head.status=='Returned')).select(db.sm_return_head.depot_id,db.sm_return_head.invoice_sl,db.sm_return_head.sl,db.sm_return_head.return_date,orderby=db.sm_return_head.sl)
    
    return dict(recordList=recordList,retRows=retRows,date_from=startDt,date_to=endDt,depot_id=depot_id,depotName=depot_name,store_id=store_id,storeName=store_name,dman_id=dman_id,delivery_man_name=delivery_man_name,territory_id=territory_id,territory_name=territory_name,mso_id=mso_id,mso_name=mso_name,customer_id=customer_id,customerName=customerName,market_id=market_id,market_name=market_name,page=page,items_per_page=items_per_page)    

    

def invoice_return_checking_download():
    c_id=session.cid
    
    response.title='30.3 Invoice wise Return Checking'
    
    fromDate=request.vars.date_from
    toDate=request.vars.date_to
    
    depot_id=str(request.vars.depot_id).strip()
    store_id=str(request.vars.store_id).strip()    
    customer_id=str(request.vars.customer_id).strip()
    #customerCat_id=str(request.vars.customerCat_id).strip()
    dman_id=str(request.vars.dman_id).strip()    
    territory_id=str(request.vars.territory_id).strip()  
    market_id=str(request.vars.market_id).strip()
    mso_id=str(request.vars.mso_id).strip()
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
    
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customer_id)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
        
    #customerCatName=''
    #clientCatRow=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customerCat_id)).select(db.sm_category_type.cat_type_name,limitby=(0,1))
    #if clientCatRow:
        #customerCatName=clientCatRow[0].cat_type_name
    
    delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==dman_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        delivery_man_name=dpRow[0].name
        
    territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        territory_name=levelRow[0].level_name
        
    market_name=''
    marketRow=db((db.sm_depot_market.cid==c_id) & (db.sm_depot_market.depot_id==depot_id) & (db.sm_depot_market.market_id==market_id)).select(db.sm_depot_market.market_name,limitby=(0,1))
    if marketRow:
        market_name=marketRow[0].market_name
        
    mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        mso_name=repRow[0].name
    
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
    
    condStr=" AND (round((sm_invoice_head.return_tp+sm_invoice_head.return_vat-sm_invoice_head.return_discount),2)!=0)"
    
    if customer_id!='':
        condStr+=" AND (sm_invoice_head.client_id='"+customer_id+"')"        
    if dman_id!='':
        condStr+=" AND (sm_invoice_head.d_man_id='"+dman_id+"')"        
    if territory_id!='':
        condStr+=" AND (sm_invoice_head.area_id='"+territory_id+"')"      
    if market_id!='':
        condStr+=" AND (sm_invoice_head.market_id='"+market_id+"')"      
    if mso_id!='':
        condStr+=" AND (sm_invoice_head.rep_id='"+mso_id+"')"        
        
    if startDt!='' and endDt!='': 
        dateRecords="SELECT sm_invoice_head.depot_id as depot_id,sm_invoice_head.invoice_date as invoice_date,sm_invoice_head.sl as invSl,sm_invoice_head.client_id as client_id,sm_invoice_head.actual_total_tp as actualTpAmt,sm_invoice_head.vat_total_amount as vatTotalAmt,sm_invoice_head.discount as discAmt,sm_invoice_head.sp_discount as spDiscAmt,sm_invoice_head.return_tp as retTpAmt,sm_invoice_head.return_vat as retVatAmt,sm_invoice_head.return_discount as retDiscAmt,sm_invoice_head.return_sp_discount as retSpDiscAmt FROM sm_invoice_head WHERE ((sm_invoice_head.cid = '"+c_id+"') AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.store_id='"+store_id+"') AND ((sm_invoice_head.invoice_date >= '"+str(startDt)+"') AND (sm_invoice_head.invoice_date <= '"+str(endDt)+"')) AND (sm_invoice_head.status='Invoiced') "+str(condStr)+") ORDER BY sm_invoice_head.sl"
    else:
        dateRecords=''
        response.flash='Required Date From and Date To'
        
    recordList=db.executesql(dateRecords,as_dict = True)
    
    invList=[]
    for i in range(len(recordList)):
        dictData=recordList[i]
        invList.append(dictData['invSl'])
        
    retRows=db((db.sm_return_head.cid==c_id)&(db.sm_return_head.depot_id==depot_id)&(db.sm_return_head.invoice_sl.belongs(invList))&(db.sm_return_head.status=='Returned')).select(db.sm_return_head.depot_id,db.sm_return_head.invoice_sl,db.sm_return_head.sl,db.sm_return_head.return_date,orderby=db.sm_return_head.sl)
    
    #-------------
    myString='30.3 Invoice wise Return Checking\n'
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depot_name)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(store_name)+'\n'
    myString+='DP ID:,'+str(dman_id)+'\n'
    myString+='DP Name'+','+str(delivery_man_name)+'\n'
    myString+='Territory ID:,'+str(territory_id)+'\n'
    myString+='Territory Name'+','+str(territory_name)+'\n'
    myString+='MSO ID:,'+str(mso_id)+'\n'
    myString+='MSO Name'+','+str(mso_name)+'\n'
    myString+='Market Name'+','+str(market_name)+'\n'
    myString+='Inv. Date From:,'+str(startDt)+'\n'            
    myString+='Inv.To Date:'+','+str(endDt)+'\n'
    
    myString+='Inv.Date,Inv.Number,Cust.ID,Invoice Net,Retn.Date,Retn.Number,Retn.Amount,Diff.Day'+'\n'
    
    totalInvAmt=0
    totalRetAmt=0
    
    for i in range(len(recordList)):
        recData=recordList[i]
    
        invAmt=round(recData['actualTpAmt']+recData['vatTotalAmt']-(recData['discAmt']+recData['spDiscAmt']),2)
        retAmt=round(recData['retTpAmt']+recData['retVatAmt']-recData['retDiscAmt'],2)
    
        totalInvAmt+=invAmt
        totalRetAmt+=retAmt
     
        retSl=''
        retDate=''
        return_date=''
        for retRow in retRows:
            invoice_sl=retRow.invoice_sl
            if invoice_sl==recData['invSl']:
                sl=str(session.prefix_invoice)+'RET'+str(retRow.depot_id)+'-'+str(retRow.sl)
                return_date=str(retRow.return_date)
                returnDate=str(retRow.return_date.strftime('%d-%b-%Y'))
             
                if retSl=='':
                    retSl=sl
                    retDate=returnDate
                else:
                    retSl+='; '+sl
                    retDate+='; '+returnDate       
        
        #-----------------        
        invoice_date=recData['invoice_date']
        invSl=str(session.prefix_invoice)+'INV'+str(recData['depot_id'])+'-'+str(recData['invSl'])
        client_id=recData['client_id']
        
        invoice_date=datetime.datetime.strptime(str(recData['invoice_date']),'%Y-%m-%d')
        return_date=datetime.datetime.strptime(str(return_date),'%Y-%m-%d')
        diffDay=(return_date-invoice_date).days
        
        #------------------------
        myString+=str(invoice_date)+','+str(invSl)+','+str(client_id)+','+str(invAmt)+','+str(retDate)+','+str(retSl)+','+str(retAmt)+','+str(diffDay)+','+'\n'
        
    myString+='Total,,,'+str(round(totalInvAmt,2))+',,,'+str(round(totalRetAmt,2))+'\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_invoice_return_checking.csv'   
    return str(myString)


def invoice_exclusive_bonus():
    c_id=session.cid
    
    response.title='30.4 Invoice Exclusive Bonus'
    
    fromDate=request.vars.date_from
    toDate=request.vars.date_to
    
    depot_id=str(request.vars.depot_id).strip()
    store_id=str(request.vars.store_id).strip()    
    customer_id=str(request.vars.customer_id).strip()    
    dman_id=str(request.vars.dman_id).strip()    
    territory_id=str(request.vars.teritory_id).strip()  
    market_id=str(request.vars.market_id).strip()
    mso_id=str(request.vars.mso_id).strip()
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
    
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customer_id)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
    
    delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==dman_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        delivery_man_name=dpRow[0].name
        
    territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        territory_name=levelRow[0].level_name
        
    market_name=''
    marketRow=db((db.sm_depot_market.cid==c_id) & (db.sm_depot_market.depot_id==depot_id) & (db.sm_depot_market.market_id==market_id)).select(db.sm_depot_market.market_name,limitby=(0,1))
    if marketRow:
        market_name=marketRow[0].market_name
        
    mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        mso_name=repRow[0].name
        
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
    
    condStr=" (sm_invoice.cid = '"+c_id+"') AND (sm_invoice.depot_id='"+depot_id+"') AND (sm_invoice.store_id='"+store_id+"') AND ((sm_invoice.invoice_date >= '"+str(startDt)+"') AND (sm_invoice.invoice_date <= '"+str(endDt)+"')) AND  (sm_invoice.status='Invoiced') AND (sm_invoice.promotion_type='BONUS' OR sm_invoice.bonus_qty>0)"
    
    if customer_id!='':
        condStr+=" AND (sm_invoice.client_id='"+customer_id+"')"        
    if dman_id!='':
        condStr+=" AND (sm_invoice.d_man_id='"+dman_id+"')"        
    if territory_id!='':
        condStr+=" AND (sm_invoice.area_id='"+territory_id+"')"      
    if market_id!='':
        condStr+=" AND (sm_invoice.market_id='"+market_id+"')"      
    if mso_id!='':
        condStr+=" AND (sm_invoice.rep_id='"+mso_id+"')"        
        
    if startDt!='' and endDt!='': 
        dateRecords="SELECT sm_invoice.invoice_date as invoice_date,sm_invoice.depot_id as depot_id,sm_invoice.sl as sl,sm_invoice.client_id as client_id,sm_invoice.area_id as area_id,sm_invoice.item_id as item_id,MAX(sm_invoice.item_name) as item_name,MAX(sm_invoice.item_unit) as item_unit,sm_invoice.circular_no as circular_no,SUM(sm_invoice.quantity) as quantity, SUM(sm_invoice.bonus_qty) as bonus_qty,SUM(sm_invoice.return_qty) as return_qty, SUM(sm_invoice.return_bonus_qty) as return_bonus_qty FROM sm_invoice WHERE ("+str(condStr)+") GROUP BY sm_invoice.sl,sm_invoice.promotion_type,sm_invoice.item_id ORDER BY sm_invoice.sl asc,sm_invoice.item_name asc,sm_invoice.quantity desc"
    else:
        dateRecords=''
        response.flash='Required Date From and Date To'
        
    recordList=db.executesql(dateRecords,as_dict = True)
    
    return dict(recordList=recordList,date_from=startDt,date_to=endDt,depot_id=depot_id,depotName=depot_name,store_id=store_id,storeName=store_name,dman_id=dman_id,delivery_man_name=delivery_man_name,territory_id=territory_id,territory_name=territory_name,mso_id=mso_id,mso_name=mso_name,customer_id=customer_id,customerName=customerName,market_id=market_id,market_name=market_name,page=page,items_per_page=items_per_page)    


def invoice_exclusive_bonus_download():
    c_id=session.cid
    
    response.title='30.4 Invoice Exclusive Bonus'
    
    fromDate=request.vars.date_from
    toDate=request.vars.date_to
    
    depot_id=str(request.vars.depot_id).strip()
    store_id=str(request.vars.store_id).strip()    
    customer_id=str(request.vars.customer_id).strip()    
    dman_id=str(request.vars.dman_id).strip()    
    territory_id=str(request.vars.territory_id).strip()  
    market_id=str(request.vars.market_id).strip()
    mso_id=str(request.vars.mso_id).strip()
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
    
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customer_id)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
    
    delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==dman_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        delivery_man_name=dpRow[0].name
        
    territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        territory_name=levelRow[0].level_name
        
    market_name=''
    marketRow=db((db.sm_depot_market.cid==c_id) & (db.sm_depot_market.depot_id==depot_id) & (db.sm_depot_market.market_id==market_id)).select(db.sm_depot_market.market_name,limitby=(0,1))
    if marketRow:
        market_name=marketRow[0].market_name
        
    mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        mso_name=repRow[0].name
        
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
    
    condStr=" (sm_invoice.cid = '"+c_id+"') AND (sm_invoice.depot_id='"+depot_id+"') AND (sm_invoice.store_id='"+store_id+"') AND ((sm_invoice.invoice_date >= '"+str(startDt)+"') AND (sm_invoice.invoice_date <= '"+str(endDt)+"')) AND  (sm_invoice.status='Invoiced') AND (sm_invoice.promotion_type='BONUS' OR sm_invoice.bonus_qty>0)"
    
    if customer_id!='':
        condStr+=" AND (sm_invoice.client_id='"+customer_id+"')"        
    if dman_id!='':
        condStr+=" AND (sm_invoice.d_man_id='"+dman_id+"')"        
    if territory_id!='':
        condStr+=" AND (sm_invoice.area_id='"+territory_id+"')"      
    if market_id!='':
        condStr+=" AND (sm_invoice.market_id='"+market_id+"')"      
    if mso_id!='':
        condStr+=" AND (sm_invoice.rep_id='"+mso_id+"')"        
        
    if startDt!='' and endDt!='': 
        dateRecords="SELECT sm_invoice.invoice_date as invoice_date,sm_invoice.depot_id as depot_id,sm_invoice.sl as sl,sm_invoice.client_id as client_id,sm_invoice.area_id as area_id,sm_invoice.item_id as item_id,MAX(sm_invoice.item_name) as item_name,MAX(sm_invoice.item_unit) as item_unit,sm_invoice.circular_no as circular_no,SUM(sm_invoice.quantity) as quantity, SUM(sm_invoice.bonus_qty) as bonus_qty,SUM(sm_invoice.return_qty) as return_qty, SUM(sm_invoice.return_bonus_qty) as return_bonus_qty FROM sm_invoice WHERE ("+str(condStr)+") GROUP BY sm_invoice.sl,sm_invoice.promotion_type,sm_invoice.item_id ORDER BY sm_invoice.sl asc,sm_invoice.item_name asc,sm_invoice.quantity desc"
    else:
        dateRecords=''
        response.flash='Required Date From and Date To'
        
    recordList=db.executesql(dateRecords,as_dict = True)
    
       
    #-------------
    myString='30.4 Invoice Exclusive Bonus\n'
    
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depot_name)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(store_name)+'\n'
    myString+='DP ID:,'+str(dman_id)+'\n'
    myString+='DP Name'+','+str(delivery_man_name)+'\n'
    myString+='Territory ID:,'+str(territory_id)+'\n'
    myString+='Territory Name'+','+str(territory_name)+'\n'
    myString+='MSO ID:,'+str(mso_id)+'\n'
    myString+='MSO Name'+','+str(mso_name)+'\n'
    myString+='Market Name'+','+str(market_name)+'\n'
    myString+='Inv. Date From:,'+str(startDt)+'\n'            
    myString+='Inv.To Date:'+','+str(endDt)+'\n'
    
    myString+='Invoice Date,Inv.No,Cust.No,Tr.Code,ItemID,Item Name,Unit,Invoice-Inv.Qnty,Invoice-Bonus Qnty,Return-Inv.Qnty,Return-Bonus Qnty,Net-Inv.Qnty,Net-Bonus Qnty,Circular No'+'\n'

    
    for i in range(len(recordList)):
        recData=recordList[i]
    
        netInvQty=recData['quantity']-recData['return_qty']
        netBonusQty=recData['bonus_qty']-recData['return_bonus_qty']
        
        #-----------------   
        invoice_date=recData['invoice_date'].strftime('%d-%m-%Y')
        sl=str(session.prefix_invoice)+'INV'+str(recData['depot_id'])+'-'+str(recData['sl'])
        client_id=recData['client_id']
        area_id=recData['area_id']
        item_id=recData['item_id']
        item_name=recData['item_name']        
        item_unit=recData['item_unit']
        quantity=recData['quantity']
        bonus_qty=recData['bonus_qty']
        return_qty=recData['return_qty']
        return_bonus_qty=recData['return_bonus_qty']
        circular_no=recData['circular_no']
        
        netInvQty=quantity-return_qty
        netBonusQty=bonus_qty-return_bonus_qty
        
        #------------------------
        myString+=str(invoice_date)+','+str(sl)+','+str(client_id)+','+str(area_id)+','+str(item_id)+','+str(item_name)+','+str(item_unit)+','+str(quantity)+','+str(bonus_qty)+','+str(return_qty)+','+str(return_bonus_qty)+','+str(netInvQty)+','+str(netBonusQty)+','+str(circular_no)+'\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_invoice_exclusive_bonus.csv'   
    return str(myString)
    
def return_note_preview():
    c_id=session.cid
    
    response.title='5.2 Return Note Preview'
    
    fromDate=request.vars.date_from
    toDate=request.vars.date_to
    
    depot_id=str(request.vars.depot_id).strip()
    store_id=str(request.vars.store_id).strip()    
    customer_id=str(request.vars.customer_id).strip()
    dman_id=str(request.vars.dman_id).strip()    
    territory_id=str(request.vars.teritory_id).strip()  
    market_id=str(request.vars.market_id).strip()
    mso_id=str(request.vars.mso_id).strip()
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
        
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customer_id)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
        
    delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==dman_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        delivery_man_name=dpRow[0].name
        
    territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        territory_name=levelRow[0].level_name
        
    market_name=''
    marketRow=db((db.sm_depot_market.cid==c_id) & (db.sm_depot_market.depot_id==depot_id) & (db.sm_depot_market.market_id==market_id)).select(db.sm_depot_market.market_name,limitby=(0,1))
    if marketRow:
        market_name=marketRow[0].market_name
        
    mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        mso_name=repRow[0].name
        
    try:        
        startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        startDt=''                
        
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    #=============================
    qset=db()
    qset=qset(db.sm_return_head.cid==c_id)
    qset=qset(db.sm_return_head.depot_id==depot_id)
    qset=qset(db.sm_return_head.store_id==store_id)    
    qset=qset((db.sm_return_head.return_date>=startDt)& (db.sm_return_head.return_date<=endDt))
    qset=qset(db.sm_return_head.status=='Returned')
    
    if customer_id!='':
        qset=qset(db.sm_return_head.client_id==customer_id)    
    if dman_id!='':
        qset=qset(db.sm_return_head.d_man_id==dman_id)  
    if territory_id!='':
        qset=qset(db.sm_return_head.area_id==territory_id)
    if market_id!='':
        qset=qset(db.sm_return_head.market_id==market_id) 
    if mso_id!='':
        qset=qset(db.sm_return_head.rep_id==mso_id)   
        
    records=qset.select(db.sm_return_head.ALL,orderby=db.sm_return_head.sl)
    
    data_List=[]
    
    for row in records:
        depot_id=row.depot_id
        depotName=row.depot_name
        store_id=row.store_id
        store_name=row.store_name
        
        sl=row.sl        
        order_sl=row.order_sl
        invoice_sl=row.invoice_sl
        return_date=row.return_date
        
        client_id=row.client_id
        client_name=row.client_name
        rep_id=row.rep_id
        rep_name=row.rep_name
        level0_name=row.level0_name
        level2_name=row.level2_name
        area_name=row.area_name
        
        discount=row.discount
        req_note=row.note
        status=row.status
        cause=row.ret_reason
        updatedBy=row.updated_by
        inv_discount=row.inv_discount
        prev_return_discount=row.prev_return_discount
        
        d_man_id=row.d_man_id      
        d_man_name=row.d_man_name
        invoice_date=row.invoice_date.strftime('%d-%b-%Y')
        cl_category_name=row.cl_category_name
        market_name=row.market_name
        
        payment_mode=''
        order_date=''
        invRecords=db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==depot_id) & (db.sm_invoice_head.sl==invoice_sl)).select(db.sm_invoice_head.payment_mode,db.sm_invoice_head.order_datetime,limitby=(0,1))
        if invRecords:            
            payment_mode=invRecords[0].payment_mode            
            order_date=invRecords[0].order_datetime.strftime('%d-%b-%Y')
        
        address=''
        contact_no1=''
        district=''
        clientRows=db((db.sm_client.cid==c_id)& (db.sm_client.depot_id==depot_id) & (db.sm_client.client_id==client_id)).select(db.sm_client.address,db.sm_client.contact_no1,db.sm_client.district,limitby=(0,1))
        if clientRows:
            address=clientRows[0].address
            contact_no1=clientRows[0].contact_no1
            district=clientRows[0].district
        
        
        detDictList=[]
        mCartonTotal=0
        detailRows=db((db.sm_return.cid==c_id)& (db.sm_return.depot_id==depot_id) & (db.sm_return.sl==sl)).select(db.sm_return.ALL,orderby=db.sm_return.item_name)
        for dRow in detailRows:        
            item_id=dRow.item_id
            item_name=dRow.item_name
            batch_id=dRow.batch_id
            item_unit=dRow.item_unit
            quantity=dRow.quantity
            bonus_qty=dRow.bonus_qty  
            price=dRow.price       
            item_vat=dRow.item_vat
            inv_quantity=dRow.inv_quantity
            inv_bonus_qty=dRow.inv_bonus_qty
            prev_return_qty=dRow.prev_return_qty
            prev_return_bonus_qty=dRow.prev_return_bonus_qty
            inv_price=dRow.inv_price
            inv_item_vat=dRow.inv_item_vat
                        
            #------------------------
            vdDict= {'item_id': item_id,'item_name': item_name,'batch_id':batch_id,'item_unit':item_unit,'quantity':quantity,'bonus_qty':bonus_qty,'price':price,'item_vat':item_vat,'inv_quantity':inv_quantity,'inv_bonus_qty': inv_bonus_qty,'prev_return_qty': prev_return_qty,'prev_return_bonus_qty': prev_return_bonus_qty,'inv_price': inv_price,'inv_item_vat': inv_item_vat}
            detDictList.append(vdDict)
            
        vhDict={'depot_id':depot_id,'depot_name':depotName,'sl':sl,'order_sl':order_sl,'invoice_sl':invoice_sl,'return_date':return_date,'client_id':client_id,'client_name':client_name,'rep_id':rep_id,'rep_name':rep_name,'req_note':req_note,'status':status,'discount':discount,'cause':cause,'updatedBy':updatedBy,'d_man_id':d_man_id,'d_man_name':d_man_name,'payment_mode':payment_mode,'inv_discount':inv_discount,'prev_return_discount':prev_return_discount,'invoice_date':invoice_date,'level0_name':level0_name,'level2_name':level2_name,'order_date':order_date,'address':address,'category_name':cl_category_name,'market_name':market_name,'contact_no1':contact_no1,'district':district,'area_name':area_name,'store_id':store_id,'store_name':store_name,'vdList':detDictList}
        data_List.append(vhDict)
    
    return dict(data_List=data_List,fromDate=fromDate,toDate=toDate,depotID=depot_id,depotName=depotName,storeID=store_id,storeName=store_name)    

    #-------------
    

def customer_sub_cat_wise_sales():
    c_id=session.cid
    
    response.title='27 Whole Sale-Retail-Institution Wise Sales Statement'
    
    fromDate=request.vars.date_from
    toDate=request.vars.date_to
    
    depot_id=str(request.vars.depot_id).strip()
    store_id=str(request.vars.store_id).strip()    
    
    customerSubCat=str(request.vars.customerSubCat).strip()  
    product_id=str(request.vars.product_id).strip()
    
      
    subCatList=[]
    customerSubCat=customerSubCat.replace('["','').replace("['","").replace("']","").replace('"]','').replace("',",",").replace(",'",",").replace(", '",",").replace('",',',').replace(', "',',')
    
    if customerSubCat=='None':
        customerSubCat=''
    subCatList=customerSubCat.split(',')    
    if subCatList[0]=='all':
        subCatList.remove('all')
    
    subCatListStr=''
    subCatNameStr=''
    for i in range(len(subCatList)):
        subCatId=subCatList[i]
        
        subCatName=''
        custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==subCatId)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
        if custSubCatRows:
            subCatName=custSubCatRows[0].cat_type_name
            
        if subCatListStr=='':
            subCatListStr="'"+str(subCatId)+"'"            
            subCatNameStr=str(subCatName)
        else:
            subCatListStr+=",'"+str(subCatId)+"'"
            subCatNameStr+=", "+str(subCatName)
    
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
    
    itemName=''
    itemRow=db((db.sm_item.cid==c_id)&(db.sm_item.item_id==product_id)).select(db.sm_item.name,limitby=(0,1))
    if itemRow:
        itemName=itemRow[0].name
        
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
    
    condStr=" (sm_invoice_head.cid = '"+c_id+"') AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.store_id='"+store_id+"') AND ((sm_invoice_head.invoice_date >= '"+str(startDt)+"') AND (sm_invoice_head.invoice_date <= '"+str(endDt)+"')) AND  (sm_invoice_head.status='Invoiced')"
    if customerSubCat!='':
        if len(subCatList)>0:            
            condStr+=" AND (sm_invoice_head.cl_sub_category_id IN ("+subCatListStr+"))"  
            
    if product_id!='':
        condStr+=" AND (sm_invoice.cid = '"+c_id+"') AND (sm_invoice.depot_id='"+depot_id+"') AND (sm_invoice.sl=sm_invoice_head.sl) AND (sm_invoice.item_id='"+product_id+"')"
        
        dataRecords="SELECT sm_invoice_head.cl_sub_category_id as cl_sub_category_id,MAX(sm_invoice_head.cl_sub_category_name) as cl_sub_category_name,sm_invoice_head.level1_id as level1_id,sm_invoice_head.level2_id as level2_id,sm_invoice_head.level3_id as level3_id,sm_invoice_head.client_id as client_id,concat(sm_invoice_head.level3_id,'-',sm_invoice_head.client_id) as headID,MAX(sm_invoice_head.client_name) as client_name,SUM(sm_invoice.actual_tp*quantity) as invTp,SUM(sm_invoice.actual_tp*return_qty) as retTp FROM sm_invoice_head, sm_invoice WHERE ("+str(condStr)+") GROUP BY sm_invoice_head.cl_sub_category_id,sm_invoice_head.level1_id,sm_invoice_head.level2_id,sm_invoice_head.level3_id,sm_invoice_head.client_id ORDER BY sm_invoice_head.cl_sub_category_id,sm_invoice_head.level1_id,sm_invoice_head.level2_id,sm_invoice_head.level3_id,sm_invoice_head.client_name"
        
    else:        
        dataRecords="SELECT sm_invoice_head.cl_sub_category_id as cl_sub_category_id,MAX(sm_invoice_head.cl_sub_category_name) as cl_sub_category_name,sm_invoice_head.level1_id as level1_id,sm_invoice_head.level2_id as level2_id,sm_invoice_head.level3_id as level3_id,sm_invoice_head.client_id as client_id,concat(sm_invoice_head.level3_id,'-',sm_invoice_head.client_id) as headID,MAX(sm_invoice_head.client_name) as client_name,SUM(sm_invoice_head.actual_total_tp) as invTp,SUM(sm_invoice_head.return_tp+sm_invoice_head.return_sp_discount) as retTp FROM sm_invoice_head WHERE ("+str(condStr)+") GROUP BY sm_invoice_head.cl_sub_category_id,sm_invoice_head.level1_id,sm_invoice_head.level2_id,sm_invoice_head.level3_id,sm_invoice_head.client_id ORDER BY sm_invoice_head.cl_sub_category_id,sm_invoice_head.level1_id,sm_invoice_head.level2_id,sm_invoice_head.level3_id,sm_invoice_head.client_name"
    
    recordList=db.executesql(dataRecords,as_dict = True)
    
    return dict(recordList=recordList,fromDate=startDt,toDate=endDt,depot_id=depot_id,depotName=depot_name,store_id=store_id,storeName=store_name,item_id=product_id,itemName=itemName,subCatNameStr=subCatNameStr,page=page,items_per_page=items_per_page)    

def covered_customer_list():
    c_id=session.cid
    
    response.title='19 Covered Customer List'
    
    fromDate=request.vars.date_from
    toDate=request.vars.date_to
    
    depot_id=str(request.vars.depot_id).strip()
    store_id=str(request.vars.store_id).strip()    
    
    customerSubCat=str(request.vars.customerSubCat).strip()  
    product_id=str(request.vars.product_id).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    level1_id=str(request.vars.level1_id).strip()
    level2_id=str(request.vars.level2_id).strip()
    
    subCatList=[]
    customerSubCat=customerSubCat.replace('["','').replace("['","").replace("']","").replace('"]','').replace("',",",").replace(",'",",").replace(", '",",").replace('",',',').replace(', "',',')
    
    if customerSubCat=='None':
        customerSubCat=''
    subCatList=customerSubCat.split(',')    
    if subCatList[0]=='all':
        subCatList.remove('all')
    
    subCatListStr=''
    subCatNameStr=''
    for i in range(len(subCatList)):
        subCatId=subCatList[i]
        
        subCatName=''
        custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==subCatId)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
        if custSubCatRows:
            subCatName=custSubCatRows[0].cat_type_name
            
        if subCatListStr=='':
            subCatListStr="'"+str(subCatId)+"'"            
            subCatNameStr=str(subCatName)
        else:
            subCatListStr+=",'"+str(subCatId)+"'"
            subCatNameStr+=", "+str(subCatName)
    
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        mso_name=repRow[0].name
        
    itemName=''
    itemRow=db((db.sm_item.cid==c_id)&(db.sm_item.item_id==product_id)).select(db.sm_item.name,limitby=(0,1))
    if itemRow:
        itemName=itemRow[0].name
        
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
    
    condStr=" (sm_invoice_head.cid = '"+c_id+"') AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.store_id='"+store_id+"') AND ((sm_invoice_head.invoice_date >= '"+str(startDt)+"') AND (sm_invoice_head.invoice_date <= '"+str(endDt)+"')) AND  (sm_invoice_head.status='Invoiced')"
    if customerSubCat!='':
        if len(subCatList)>0:            
            condStr+=" AND (sm_invoice_head.cl_sub_category_id IN ("+subCatListStr+"))"  
    
    if mso_id!='':
        condStr+=" AND (sm_invoice_head.rep_id='"+mso_id+"')" 
    if level1_id!='':
        condStr+=" AND (sm_invoice_head.level1_id='"+level1_id+"')" 
    if level2_id!='':
        condStr+=" AND (sm_invoice_head.level2_id='"+level2_id+"')" 
        
    if product_id!='':
        condStr+=" AND (sm_invoice.cid = '"+c_id+"') AND (sm_invoice.depot_id='"+depot_id+"') AND (sm_invoice.sl=sm_invoice_head.sl) AND (sm_invoice.item_id='"+product_id+"')"
        
        dataRecords="SELECT sm_invoice_head.level1_id as level1_id,sm_invoice_head.level2_id as level2_id,sm_invoice_head.level3_id as level3_id,sm_invoice_head.client_id as client_id,concat(sm_invoice_head.level3_id,'-',sm_invoice_head.client_id) as headID,MAX(sm_invoice_head.client_name) as client_name,MAX(sm_invoice_head.market_name) as market_name,COUNT(distinct(sm_invoice.sl)) as invCount,SUM(sm_invoice_head.return_count) as retCount,SUM(sm_invoice.actual_tp*quantity) as invTp,SUM(sm_invoice.actual_tp*return_qty) as retTp FROM sm_invoice_head, sm_invoice WHERE ("+str(condStr)+") GROUP BY sm_invoice_head.level1_id,sm_invoice_head.level2_id,sm_invoice_head.level3_id,sm_invoice_head.client_id ORDER BY sm_invoice_head.level1_id,sm_invoice_head.level2_id,sm_invoice_head.level3_id,sm_invoice_head.client_name"
        
    else:        
        dataRecords="SELECT sm_invoice_head.level1_id as level1_id,sm_invoice_head.level2_id as level2_id,sm_invoice_head.level3_id as level3_id,sm_invoice_head.client_id as client_id,concat(sm_invoice_head.level3_id,'-',sm_invoice_head.client_id) as headID,MAX(sm_invoice_head.client_name) as client_name,MAX(sm_invoice_head.market_name) as market_name,COUNT(distinct(sm_invoice_head.sl)) as invCount,SUM(sm_invoice_head.return_count) as retCount,SUM(sm_invoice_head.actual_total_tp) as invTp,SUM(sm_invoice_head.return_tp+sm_invoice_head.return_sp_discount) as retTp FROM sm_invoice_head WHERE ("+str(condStr)+") GROUP BY sm_invoice_head.level1_id,sm_invoice_head.level2_id,sm_invoice_head.level3_id,sm_invoice_head.client_id ORDER BY sm_invoice_head.level1_id,sm_invoice_head.level2_id,sm_invoice_head.level3_id,sm_invoice_head.client_name"
        
    recordList=db.executesql(dataRecords,as_dict = True)
    
    return dict(recordList=recordList,date_from=startDt,date_to=endDt,depot_id=depot_id,depotName=depot_name,store_id=store_id,storeName=store_name,product_id=product_id,itemName=itemName,subCatNameStr=subCatNameStr,mso_id=mso_id,mso_name=mso_name,level1_id=level1_id,level2_id=level2_id,customerSubCat=customerSubCat,page=page,items_per_page=items_per_page)    
    

def covered_customer_list_download():
    c_id=session.cid
    
    response.title='19 Download-Covered Customer List'
    
    fromDate=request.vars.date_from
    toDate=request.vars.date_to
    
    depot_id=str(request.vars.depot_id).strip()
    store_id=str(request.vars.store_id).strip()    
    
    customerSubCat=str(request.vars.customerSubCat).strip()  
    product_id=str(request.vars.product_id).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    level1_id=str(request.vars.level1_id).strip()
    level2_id=str(request.vars.level2_id).strip()
    
    subCatList=[]
    customerSubCat=customerSubCat.replace('["','').replace("['","").replace("']","").replace('"]','').replace("',",",").replace(",'",",").replace(", '",",").replace('",',',').replace(', "',',')
    
    if customerSubCat=='None':
        customerSubCat=''
    subCatList=customerSubCat.split(',')    
    if subCatList[0]=='all':
        subCatList.remove('all')
    
    subCatListStr=''
    subCatNameStr=''
    for i in range(len(subCatList)):
        subCatId=subCatList[i]
        
        subCatName=''
        custSubCatRows=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_SUB_CATEGORY')&(db.sm_category_type.cat_type_id==subCatId)).select(db.sm_category_type.cat_type_name, limitby=(0,1))
        if custSubCatRows:
            subCatName=custSubCatRows[0].cat_type_name
            
        if subCatListStr=='':
            subCatListStr="'"+str(subCatId)+"'"            
            subCatNameStr=str(subCatName)
        else:
            subCatListStr+=",'"+str(subCatId)+"'"
            subCatNameStr+=", "+str(subCatName)
    
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        mso_name=repRow[0].name
        
    itemName=''
    itemRow=db((db.sm_item.cid==c_id)&(db.sm_item.item_id==product_id)).select(db.sm_item.name,limitby=(0,1))
    if itemRow:
        itemName=itemRow[0].name
        
    try:        
        startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        startDt=''
    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    #--------------paging
    
    condStr=" (sm_invoice_head.cid = '"+c_id+"') AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.store_id='"+store_id+"') AND ((sm_invoice_head.invoice_date >= '"+str(startDt)+"') AND (sm_invoice_head.invoice_date <= '"+str(endDt)+"')) AND  (sm_invoice_head.status='Invoiced')"
    if customerSubCat!='':
        if len(subCatList)>0:            
            condStr+=" AND (sm_invoice_head.cl_sub_category_id IN ("+subCatListStr+"))"  
    
    if mso_id!='':
        condStr+=" AND (sm_invoice_head.rep_id='"+mso_id+"')" 
    if level1_id!='':
        condStr+=" AND (sm_invoice_head.level1_id='"+level1_id+"')" 
    if level2_id!='':
        condStr+=" AND (sm_invoice_head.level2_id='"+level2_id+"')" 
        
    if product_id!='':
        condStr+=" AND (sm_invoice.cid = '"+c_id+"') AND (sm_invoice.depot_id='"+depot_id+"') AND (sm_invoice.sl=sm_invoice_head.sl) AND (sm_invoice.item_id='"+product_id+"')"
        
        dataRecords="SELECT sm_invoice_head.level1_id as level1_id,sm_invoice_head.level2_id as level2_id,sm_invoice_head.level3_id as level3_id,sm_invoice_head.client_id as client_id,concat(sm_invoice_head.level3_id,'-',sm_invoice_head.client_id) as headID,MAX(sm_invoice_head.client_name) as client_name,MAX(sm_invoice_head.market_name) as market_name,COUNT(distinct(sm_invoice.sl)) as invCount,SUM(sm_invoice_head.return_count) as retCount,SUM(sm_invoice.actual_tp*quantity) as invTp,SUM(sm_invoice.actual_tp*return_qty) as retTp FROM sm_invoice_head, sm_invoice WHERE ("+str(condStr)+") GROUP BY sm_invoice_head.level1_id,sm_invoice_head.level2_id,sm_invoice_head.level3_id,sm_invoice_head.client_id ORDER BY sm_invoice_head.level1_id,sm_invoice_head.level2_id,sm_invoice_head.level3_id,sm_invoice_head.client_name"
        
    else:        
        dataRecords="SELECT sm_invoice_head.level1_id as level1_id,sm_invoice_head.level2_id as level2_id,sm_invoice_head.level3_id as level3_id,sm_invoice_head.client_id as client_id,concat(sm_invoice_head.level3_id,'-',sm_invoice_head.client_id) as headID,MAX(sm_invoice_head.client_name) as client_name,MAX(sm_invoice_head.market_name) as market_name,COUNT(distinct(sm_invoice_head.sl)) as invCount,SUM(sm_invoice_head.return_count) as retCount,SUM(sm_invoice_head.actual_total_tp) as invTp,SUM(sm_invoice_head.return_tp+sm_invoice_head.return_sp_discount) as retTp FROM sm_invoice_head WHERE ("+str(condStr)+") GROUP BY sm_invoice_head.level1_id,sm_invoice_head.level2_id,sm_invoice_head.level3_id,sm_invoice_head.client_id ORDER BY sm_invoice_head.level1_id,sm_invoice_head.level2_id,sm_invoice_head.level3_id,sm_invoice_head.client_name"
        
    recordList=db.executesql(dataRecords,as_dict = True)
    
    #-------------
    myString='19 Covered Customer List\n'    
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depot_name)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(store_name)+'\n'
    #myString+='DP ID:,'+str(dman_id)+'\n'
    #myString+='DP Name'+','+str(delivery_man_name)+'\n'
    #myString+='Territory ID:,'+str(territory_id)+'\n'
    #myString+='Territory Name'+','+str(territory_name)+'\n'
    myString+='MSO ID:,'+str(mso_id)+'\n'
    myString+='MSO Name'+','+str(mso_name)+'\n'
    #myString+='Market Name'+','+str(market_name)+'\n'
    myString+='Inv. Date From:,'+str(startDt)+'\n'            
    myString+='Inv.To Date:'+','+str(endDt)+'\n'
    
    myString+=str(session.level1Name)+','+str(level1_id)+'\n'
    myString+=str(session.level2Name)+','+str(level2_id)+'\n'
    
    myString+='Customer -Sub.Category:'+','+str(subCatNameStr)+'\n\n'
    
    
    myString+='RSM Tr. Code,FM Tr. Code,MSO Tr. Code,Cust.ID,Customer Name,Cust.Market,Covered Cust.,InvCount,RetCount,Ret%,Invocie TP,Return TP,Net Price'+'\n'
    
    
    rowSL=0
    
    invGrandTotal=0
    retGrandTotal=0
    
    #<!--RSM-->
    
    
    #<!--FM-->
    
    
    #<!--MSO-->
        
    for i in range(len(recordList)):  
        
        recData=recordList[i]
        level1_id=recData['level1_id']
        level2_id=recData['level2_id']
        level3_id=recData['level3_id']
        
        invAmt_0=round(float(recData['invTp']),2)
                
        retAmt_1=round(float(recData['retTp']),2)
                
        netPrice=round(invAmt_0-retAmt_1,2)
        
        invGrandTotal+=invAmt_0
        retGrandTotal+=retAmt_1        
        if netPrice==0:
            executePercent=0
            retPercent=0
        else:
            try:
                executePercent=round((netPrice*100)/invAmt_0,2)
                retPercent=round(100-executePercent,2)
            except:
                executePercent=0
                retPercent=0
            
        rowSL+=1
        
        myString+=str(level1_id)+','+str(level2_id)+','+str(level3_id)+','+str(recData['client_id'])+','+str(recData['client_name'])+','+str(recData['market_name'])+',,'+str(recData['invCount'])+','+str(recData['retCount'])+',,'+str(invAmt_0)+','+str(retAmt_1)+','+str(netPrice)+'\n'
        
      #<!-- End Details-->
    
    #------------------------
    
    #myString+=str(invocieCount)+' Invoice(s),Total,,,,,,,'+str(round(invTpTotal,2))+','+str(round(invDiscTotal,2))+','+str(round(invVatTotal,2))+','+str(round(invNetTotal,2))+','+str(round(retTpTotal,2))+','+str(round(retDiscTotal,2))+','+str(round(retVatTotal,2))+','+str(round(retNetTotal,2))+','+str(round(netTpTotal,2))+','+str(round(netDiscTotal,2))+','+str(round(netVatTotal,2))+','+str(round(netGrandTotal,2))+'\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_covered_customer_list.csv'   
    return str(myString)
    
def discount_type_wise_sales():
    c_id=session.cid
    
    response.title='9A Discount Type Wise Sales'
    
    fromDate=request.vars.date_from
    toDate=request.vars.date_to
    
    depot_id=str(request.vars.depot_id).strip()
    store_id=str(request.vars.store_id).strip()    
    customer_id=str(request.vars.customer_id).strip()
    #customerCat_id=str(request.vars.customerCat_id).strip()
    dman_id=str(request.vars.dman_id).strip()    
    territory_id=str(request.vars.teritory_id).strip()  
    market_id=str(request.vars.market_id).strip()
    mso_id=str(request.vars.mso_id).strip()
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
    
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customer_id)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
        
    #customerCatName=''
    #clientCatRow=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customerCat_id)).select(db.sm_category_type.cat_type_name,limitby=(0,1))
    #if clientCatRow:
        #customerCatName=clientCatRow[0].cat_type_name
    
    delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==dman_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        delivery_man_name=dpRow[0].name
        
    territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        territory_name=levelRow[0].level_name
        
    market_name=''
    marketRow=db((db.sm_depot_market.cid==c_id) & (db.sm_depot_market.depot_id==depot_id) & (db.sm_depot_market.market_id==market_id)).select(db.sm_depot_market.market_name,limitby=(0,1))
    if marketRow:
        market_name=marketRow[0].market_name
        
    mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        mso_name=repRow[0].name
    
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
    
    condStr=" (sm_invoice_head.cid = '"+c_id+"') AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.store_id='"+store_id+"') AND ((sm_invoice_head.invoice_date >= '"+str(startDt)+"') AND (sm_invoice_head.invoice_date <= '"+str(endDt)+"')) AND  (sm_invoice_head.status='Invoiced')"
    
    if customer_id!='':
        condStr+=" AND (sm_invoice_head.client_id='"+customer_id+"')"        
    if dman_id!='':
        condStr+=" AND (sm_invoice_head.d_man_id='"+dman_id+"')"        
    if territory_id!='':
        condStr+=" AND (sm_invoice_head.area_id='"+territory_id+"')"      
    if market_id!='':
        condStr+=" AND (sm_invoice_head.market_id='"+market_id+"')"      
    if mso_id!='':
        condStr+=" AND (sm_invoice_head.rep_id='"+mso_id+"')"        
        
    if startDt!='' and endDt!='': 
        dateRecords="SELECT sm_invoice_head.depot_id as depot_id,sm_invoice_head.invoice_date as invoice_date,sm_invoice_head.sl as invSl,sm_invoice_head.client_id as client_id,sm_invoice_head.client_name as client_name,sm_invoice_head.area_id as area_id,sm_invoice_head.market_name as market_name,sm_invoice_head.actual_total_tp as actualTpAmt,sm_invoice_head.regular_disc_tp as regular_disc_tp,sm_invoice_head.flat_disc_tp as flat_disc_tp,sm_invoice_head.approved_disc_tp as approved_disc_tp,sm_invoice_head.others_disc_tp as others_disc_tp,sm_invoice_head.no_disc_tp as no_disc_tp,sm_invoice_head.ret_actual_total_tp as ret_actual_total_tp,sm_invoice_head.ret_regular_disc_tp as ret_regular_disc_tp,sm_invoice_head.ret_flat_disc_tp as ret_flat_disc_tp,sm_invoice_head.ret_approved_disc_tp as ret_approved_disc_tp,sm_invoice_head.ret_others_disc_tp as ret_others_disc_tp,sm_invoice_head.vat_total_amount as vatTotalAmt,sm_invoice_head.discount as discAmt,sm_invoice_head.sp_discount as spDiscAmt,sm_invoice_head.sp_flat as spFlatDiscAmt,sm_invoice_head.sp_approved as spApprovedDiscAmt,sm_invoice_head.sp_others as spOthersDiscAmt,sm_invoice_head.ret_sp_flat as ret_sp_flat,sm_invoice_head.ret_sp_approved as ret_sp_approved,sm_invoice_head.ret_sp_others as ret_sp_others,sm_invoice_head.return_tp as retTpAmt,sm_invoice_head.return_vat as retVatAmt,sm_invoice_head.return_discount as retDiscAmt,sm_invoice_head.return_sp_discount as retSpDiscAmt,sm_invoice_head.discount_precent as discount_precent FROM sm_invoice_head WHERE ("+str(condStr)+") ORDER BY sm_invoice_head.sl"
    else:
        dateRecords=''
        response.flash='Required Date From and Date To'
        
    recordList=db.executesql(dateRecords,as_dict = True)
    invocieCount=len(recordList)
    
    return dict(recordList=recordList,invocieCount=invocieCount,date_from=startDt,date_to=endDt,depot_id=depot_id,depotName=depot_name,store_id=store_id,storeName=store_name,dman_id=dman_id,delivery_man_name=delivery_man_name,territory_id=territory_id,territory_name=territory_name,mso_id=mso_id,mso_name=mso_name,customer_id=customer_id,customerName=customerName,market_id=market_id,market_name=market_name,page=page,items_per_page=items_per_page)    
    

def discount_type_wise_sales_ad():
    c_id=session.cid
    
    response.title='9B Discount Type Wise Sales-AD'
    
    fromDate=request.vars.date_from
    toDate=request.vars.date_to
    
    depot_id=str(request.vars.depot_id).strip()
    store_id=str(request.vars.store_id).strip()    
    customer_id=str(request.vars.customer_id).strip()
    #customerCat_id=str(request.vars.customerCat_id).strip()
    dman_id=str(request.vars.dman_id).strip()    
    territory_id=str(request.vars.teritory_id).strip()  
    market_id=str(request.vars.market_id).strip()
    mso_id=str(request.vars.mso_id).strip()
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
    
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customer_id)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
        
    #customerCatName=''
    #clientCatRow=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customerCat_id)).select(db.sm_category_type.cat_type_name,limitby=(0,1))
    #if clientCatRow:
        #customerCatName=clientCatRow[0].cat_type_name
    
    delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==dman_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        delivery_man_name=dpRow[0].name
        
    territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        territory_name=levelRow[0].level_name
        
    market_name=''
    marketRow=db((db.sm_depot_market.cid==c_id) & (db.sm_depot_market.depot_id==depot_id) & (db.sm_depot_market.market_id==market_id)).select(db.sm_depot_market.market_name,limitby=(0,1))
    if marketRow:
        market_name=marketRow[0].market_name
        
    mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        mso_name=repRow[0].name
    
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
    
    condStr=" (sm_invoice_head.cid = '"+c_id+"') AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.store_id='"+store_id+"') AND ((sm_invoice_head.invoice_date >= '"+str(startDt)+"') AND (sm_invoice_head.invoice_date <= '"+str(endDt)+"')) AND  (sm_invoice_head.status='Invoiced')"
    
    if customer_id!='':
        condStr+=" AND (sm_invoice_head.client_id='"+customer_id+"')"        
    if dman_id!='':
        condStr+=" AND (sm_invoice_head.d_man_id='"+dman_id+"')"        
    if territory_id!='':
        condStr+=" AND (sm_invoice_head.area_id='"+territory_id+"')"      
    if market_id!='':
        condStr+=" AND (sm_invoice_head.market_id='"+market_id+"')"      
    if mso_id!='':
        condStr+=" AND (sm_invoice_head.rep_id='"+mso_id+"')"        
        
    if startDt!='' and endDt!='': 
        dateRecords="SELECT sm_invoice_head.depot_id as depot_id,sm_invoice_head.invoice_date as invoice_date,sm_invoice_head.sl as invSl,sm_invoice_head.client_id as client_id,sm_invoice_head.client_name as client_name,sm_invoice_head.area_id as area_id,sm_invoice_head.market_name as market_name,sm_invoice_head.actual_total_tp as actualTpAmt,sm_invoice_head.regular_disc_tp as regular_disc_tp,sm_invoice_head.flat_disc_tp as flat_disc_tp,sm_invoice_head.approved_disc_tp as approved_disc_tp,sm_invoice_head.others_disc_tp as others_disc_tp,sm_invoice_head.no_disc_tp as no_disc_tp,sm_invoice_head.ret_actual_total_tp as ret_actual_total_tp,sm_invoice_head.ret_regular_disc_tp as ret_regular_disc_tp,sm_invoice_head.ret_flat_disc_tp as ret_flat_disc_tp,sm_invoice_head.ret_approved_disc_tp as ret_approved_disc_tp,sm_invoice_head.ret_others_disc_tp as ret_others_disc_tp,sm_invoice_head.vat_total_amount as vatTotalAmt,sm_invoice_head.discount as discAmt,sm_invoice_head.sp_discount as spDiscAmt,sm_invoice_head.sp_flat as spFlatDiscAmt,sm_invoice_head.sp_approved as spApprovedDiscAmt,sm_invoice_head.sp_others as spOthersDiscAmt,sm_invoice_head.ret_sp_flat as ret_sp_flat,sm_invoice_head.ret_sp_approved as ret_sp_approved,sm_invoice_head.ret_sp_others as ret_sp_others,sm_invoice_head.return_tp as retTpAmt,sm_invoice_head.return_vat as retVatAmt,sm_invoice_head.return_discount as retDiscAmt,sm_invoice_head.return_sp_discount as retSpDiscAmt,sm_invoice_head.discount_precent as discount_precent FROM sm_invoice_head WHERE ("+str(condStr)+") ORDER BY sm_invoice_head.sl"
    else:
        dateRecords=''
        response.flash='Required Date From and Date To'
        
    recordList=db.executesql(dateRecords,as_dict = True)
    invocieCount=len(recordList)
    
    return dict(recordList=recordList,invocieCount=invocieCount,date_from=startDt,date_to=endDt,depot_id=depot_id,depotName=depot_name,store_id=store_id,storeName=store_name,dman_id=dman_id,delivery_man_name=delivery_man_name,territory_id=territory_id,territory_name=territory_name,mso_id=mso_id,mso_name=mso_name,customer_id=customer_id,customerName=customerName,market_id=market_id,market_name=market_name,page=page,items_per_page=items_per_page)    
    
def discount_type_wise_sales_with_tp():
    c_id=session.cid
    
    response.title='9C Discount Type Wise Sales-With TP'
    
    fromDate=request.vars.date_from
    toDate=request.vars.date_to
    
    depot_id=str(request.vars.depot_id).strip()
    store_id=str(request.vars.store_id).strip()    
    customer_id=str(request.vars.customer_id).strip()    
    dman_id=str(request.vars.dman_id).strip()    
    territory_id=str(request.vars.teritory_id).strip()  
    market_id=str(request.vars.market_id).strip()
    mso_id=str(request.vars.mso_id).strip()
    discount_type=str(request.vars.discount_type).strip()
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
    
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customer_id)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
        
    delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==dman_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        delivery_man_name=dpRow[0].name
        
    territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        territory_name=levelRow[0].level_name
        
    market_name=''
    marketRow=db((db.sm_depot_market.cid==c_id) & (db.sm_depot_market.depot_id==depot_id) & (db.sm_depot_market.market_id==market_id)).select(db.sm_depot_market.market_name,limitby=(0,1))
    if marketRow:
        market_name=marketRow[0].market_name
        
    mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        mso_name=repRow[0].name
    
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
    
    condStr=" (sm_invoice_head.cid = '"+c_id+"') AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.store_id='"+store_id+"') AND ((sm_invoice_head.invoice_date >= '"+str(startDt)+"') AND (sm_invoice_head.invoice_date <= '"+str(endDt)+"')) AND  (sm_invoice_head.status='Invoiced')"
    
    if customer_id!='':
        condStr+=" AND (sm_invoice_head.client_id='"+customer_id+"')"        
    if dman_id!='':
        condStr+=" AND (sm_invoice_head.d_man_id='"+dman_id+"')"        
    if territory_id!='':
        condStr+=" AND (sm_invoice_head.area_id='"+territory_id+"')"      
    if market_id!='':
        condStr+=" AND (sm_invoice_head.market_id='"+market_id+"')"      
    if mso_id!='':
        condStr+=" AND (sm_invoice_head.rep_id='"+mso_id+"')"        
        
    dateRecords=''
    if discount_type=='REGULAR':
        dateRecords="SELECT sm_invoice_head.depot_id as depot_id,sm_invoice_head.invoice_date as invoice_date,sm_invoice_head.sl as invSl,sm_invoice_head.client_id as client_id,sm_invoice_head.client_name as client_name,sm_invoice_head.area_id as area_id,sm_invoice_head.market_name as market_name,sm_invoice_head.discount_precent as discount_precent,sm_invoice_head.regular_disc_tp as invTp,sm_invoice_head.discount as invDiscAmt,(sm_invoice_head.regular_disc_tp-sm_invoice_head.ret_regular_disc_tp) as tp_amt,(sm_invoice_head.discount-sm_invoice_head.return_discount) as disc_value FROM sm_invoice_head WHERE ("+str(condStr)+" AND (sm_invoice_head.regular_disc_tp-sm_invoice_head.ret_regular_disc_tp)>0) ORDER BY sm_invoice_head.sl"
        
    elif discount_type=='FLAT':
        dateRecords="SELECT sm_invoice_head.depot_id as depot_id,sm_invoice_head.invoice_date as invoice_date,sm_invoice_head.sl as invSl,sm_invoice_head.client_id as client_id,sm_invoice_head.client_name as client_name,sm_invoice_head.area_id as area_id,sm_invoice_head.market_name as market_name,sm_invoice_head.discount_precent as discount_precent,sm_invoice_head.flat_disc_tp as invTp,sm_invoice_head.sp_flat as invDiscAmt,(sm_invoice_head.flat_disc_tp-sm_invoice_head.ret_flat_disc_tp) as tp_amt,(sm_invoice_head.sp_flat-sm_invoice_head.ret_sp_flat) as disc_value FROM sm_invoice_head WHERE ("+str(condStr)+" AND (sm_invoice_head.flat_disc_tp-sm_invoice_head.ret_flat_disc_tp)>0) ORDER BY sm_invoice_head.sl"
        
    elif discount_type=='APPROVED':
        dateRecords="SELECT sm_invoice_head.depot_id as depot_id,sm_invoice_head.invoice_date as invoice_date,sm_invoice_head.sl as invSl,sm_invoice_head.client_id as client_id,sm_invoice_head.client_name as client_name,sm_invoice_head.area_id as area_id,sm_invoice_head.market_name as market_name,sm_invoice_head.discount_precent as discount_precent,sm_invoice_head.approved_disc_tp as invTp,sm_invoice_head.sp_approved as invDiscAmt,(sm_invoice_head.approved_disc_tp-sm_invoice_head.ret_approved_disc_tp) as tp_amt,(sm_invoice_head.sp_approved-sm_invoice_head.ret_sp_approved) as disc_value FROM sm_invoice_head WHERE ("+str(condStr)+" AND (sm_invoice_head.approved_disc_tp-sm_invoice_head.ret_approved_disc_tp)>0) ORDER BY sm_invoice_head.sl"
        
    elif discount_type=='OTHERS':
        dateRecords="SELECT sm_invoice_head.depot_id as depot_id,sm_invoice_head.invoice_date as invoice_date,sm_invoice_head.sl as invSl,sm_invoice_head.client_id as client_id,sm_invoice_head.client_name as client_name,sm_invoice_head.area_id as area_id,sm_invoice_head.market_name as market_name,sm_invoice_head.discount_precent as discount_precent,sm_invoice_head.others_disc_tp as invTp,sm_invoice_head.sp_others as invDiscAmt,(sm_invoice_head.others_disc_tp-sm_invoice_head.ret_others_disc_tp) as tp_amt,(sm_invoice_head.sp_others-sm_invoice_head.ret_sp_others) as disc_value FROM sm_invoice_head WHERE ("+str(condStr)+" AND (sm_invoice_head.others_disc_tp-sm_invoice_head.ret_others_disc_tp)>0) ORDER BY sm_invoice_head.sl"
        
    elif discount_type=='NODISC':
        dateRecords="SELECT sm_invoice_head.depot_id as depot_id,sm_invoice_head.invoice_date as invoice_date,sm_invoice_head.sl as invSl,sm_invoice_head.client_id as client_id,sm_invoice_head.client_name as client_name,sm_invoice_head.area_id as area_id,sm_invoice_head.market_name as market_name,sm_invoice_head.discount_precent as discount_precent,sm_invoice_head.actual_total_tp as invTp,sm_invoice_head.no_disc_tp as invDiscAmt,(sm_invoice_head.no_disc_tp-(sm_invoice_head.ret_actual_total_tp-(sm_invoice_head.ret_regular_disc_tp+sm_invoice_head.ret_flat_disc_tp+sm_invoice_head.ret_approved_disc_tp+sm_invoice_head.ret_others_disc_tp))) as tp_amt,0 as disc_value FROM sm_invoice_head WHERE ("+str(condStr)+" AND (sm_invoice_head.no_disc_tp-(sm_invoice_head.ret_actual_total_tp-(sm_invoice_head.ret_regular_disc_tp+sm_invoice_head.ret_flat_disc_tp+sm_invoice_head.ret_approved_disc_tp+sm_invoice_head.ret_others_disc_tp)))!=0) ORDER BY sm_invoice_head.sl"
        
    recordList=db.executesql(dateRecords,as_dict = True)
    invocieCount=len(recordList)
    
    return dict(recordList=recordList,discount_type=discount_type,invocieCount=invocieCount,date_from=startDt,date_to=endDt,depot_id=depot_id,depotName=depot_name,store_id=store_id,storeName=store_name,dman_id=dman_id,delivery_man_name=delivery_man_name,territory_id=territory_id,territory_name=territory_name,mso_id=mso_id,mso_name=mso_name,customer_id=customer_id,customerName=customerName,market_id=market_id,market_name=market_name,page=page,items_per_page=items_per_page)    
    

def discount_type_wise_sales_with_value():
    c_id=session.cid
    
    response.title='9B Discount Type Wise Sales-2'
    
    fromDate=request.vars.date_from
    toDate=request.vars.date_to
    
    depot_id=str(request.vars.depot_id).strip()
    store_id=str(request.vars.store_id).strip()    
    customer_id=str(request.vars.customer_id).strip()
    #customerCat_id=str(request.vars.customerCat_id).strip()
    dman_id=str(request.vars.dman_id).strip()    
    territory_id=str(request.vars.teritory_id).strip()  
    market_id=str(request.vars.market_id).strip()
    mso_id=str(request.vars.mso_id).strip()
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
    
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customer_id)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
        
    #customerCatName=''
    #clientCatRow=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customerCat_id)).select(db.sm_category_type.cat_type_name,limitby=(0,1))
    #if clientCatRow:
        #customerCatName=clientCatRow[0].cat_type_name
    
    delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==dman_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        delivery_man_name=dpRow[0].name
        
    territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        territory_name=levelRow[0].level_name
        
    market_name=''
    marketRow=db((db.sm_depot_market.cid==c_id) & (db.sm_depot_market.depot_id==depot_id) & (db.sm_depot_market.market_id==market_id)).select(db.sm_depot_market.market_name,limitby=(0,1))
    if marketRow:
        market_name=marketRow[0].market_name
        
    mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        mso_name=repRow[0].name
    
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
    
    condStr=" (sm_invoice_head.cid = '"+c_id+"') AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.store_id='"+store_id+"') AND ((sm_invoice_head.invoice_date >= '"+str(startDt)+"') AND (sm_invoice_head.invoice_date <= '"+str(endDt)+"')) AND  (sm_invoice_head.status='Invoiced')"
    
    if customer_id!='':
        condStr+=" AND (sm_invoice_head.client_id='"+customer_id+"')"        
    if dman_id!='':
        condStr+=" AND (sm_invoice_head.d_man_id='"+dman_id+"')"        
    if territory_id!='':
        condStr+=" AND (sm_invoice_head.area_id='"+territory_id+"')"      
    if market_id!='':
        condStr+=" AND (sm_invoice_head.market_id='"+market_id+"')"      
    if mso_id!='':
        condStr+=" AND (sm_invoice_head.rep_id='"+mso_id+"')"        
        
    if startDt!='' and endDt!='': 
        dateRecords="SELECT sm_invoice_head.depot_id as depot_id,sm_invoice_head.invoice_date as invoice_date,sm_invoice_head.sl as invSl,sm_invoice_head.client_id as client_id,sm_invoice_head.client_name as client_name,sm_invoice_head.area_id as area_id,sm_invoice_head.market_name as market_name,sm_invoice_head.actual_total_tp as actualTpAmt,sm_invoice_head.regular_disc_tp as regular_disc_tp,sm_invoice_head.flat_disc_tp as flat_disc_tp,sm_invoice_head.approved_disc_tp as approved_disc_tp,sm_invoice_head.others_disc_tp as others_disc_tp,sm_invoice_head.no_disc_tp as no_disc_tp,sm_invoice_head.vat_total_amount as vatTotalAmt,sm_invoice_head.discount as discAmt,sm_invoice_head.sp_discount as spDiscAmt,sm_invoice_head.sp_flat as spFlatDiscAmt,sm_invoice_head.sp_approved as spApprovedDiscAmt,sm_invoice_head.sp_others as spOthersDiscAmt,sm_invoice_head.return_tp as retTpAmt,sm_invoice_head.return_vat as retVatAmt,sm_invoice_head.return_discount as retDiscAmt,sm_invoice_head.return_sp_discount as retSpDiscAmt,sm_invoice_head.discount_precent as discount_precent FROM sm_invoice_head WHERE ("+str(condStr)+") ORDER BY sm_invoice_head.sl"
    else:
        dateRecords=''
        response.flash='Required Date From and Date To'
        
    recordList=db.executesql(dateRecords,as_dict = True)
    invocieCount=len(recordList)
    
    return dict(recordList=recordList,invocieCount=invocieCount,date_from=startDt,date_to=endDt,depot_id=depot_id,depotName=depot_name,store_id=store_id,storeName=store_name,dman_id=dman_id,delivery_man_name=delivery_man_name,territory_id=territory_id,territory_name=territory_name,mso_id=mso_id,mso_name=mso_name,customer_id=customer_id,customerName=customerName,market_id=market_id,market_name=market_name,page=page,items_per_page=items_per_page)    
    

def discount_type_wise_sales_first():
    c_id=session.cid
    
    response.title='9A Discount Type Wise Sales'
    
    fromDate=request.vars.date_from
    toDate=request.vars.date_to
    
    depot_id=str(request.vars.depot_id).strip()
    store_id=str(request.vars.store_id).strip()    
    customer_id=str(request.vars.customer_id).strip()
    #customerCat_id=str(request.vars.customerCat_id).strip()
    dman_id=str(request.vars.dman_id).strip()    
    territory_id=str(request.vars.teritory_id).strip()  
    market_id=str(request.vars.market_id).strip()
    mso_id=str(request.vars.mso_id).strip()
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
    
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customer_id)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
        
    #customerCatName=''
    #clientCatRow=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customerCat_id)).select(db.sm_category_type.cat_type_name,limitby=(0,1))
    #if clientCatRow:
        #customerCatName=clientCatRow[0].cat_type_name
    
    delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==dman_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        delivery_man_name=dpRow[0].name
        
    territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        territory_name=levelRow[0].level_name
        
    market_name=''
    marketRow=db((db.sm_depot_market.cid==c_id) & (db.sm_depot_market.depot_id==depot_id) & (db.sm_depot_market.market_id==market_id)).select(db.sm_depot_market.market_name,limitby=(0,1))
    if marketRow:
        market_name=marketRow[0].market_name
        
    mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        mso_name=repRow[0].name
    
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
    
    condStr=" (sm_invoice_head.cid = '"+c_id+"') AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.store_id='"+store_id+"') AND ((sm_invoice_head.invoice_date >= '"+str(startDt)+"') AND (sm_invoice_head.invoice_date <= '"+str(endDt)+"')) AND  (sm_invoice_head.status='Invoiced')"
    
    if customer_id!='':
        condStr+=" AND (sm_invoice_head.client_id='"+customer_id+"')"        
    if dman_id!='':
        condStr+=" AND (sm_invoice_head.d_man_id='"+dman_id+"')"        
    if territory_id!='':
        condStr+=" AND (sm_invoice_head.area_id='"+territory_id+"')"      
    if market_id!='':
        condStr+=" AND (sm_invoice_head.market_id='"+market_id+"')"      
    if mso_id!='':
        condStr+=" AND (sm_invoice_head.rep_id='"+mso_id+"')"        
        
    if startDt!='' and endDt!='': 
        dateRecords="SELECT sm_invoice_head.depot_id as depot_id,sm_invoice_head.invoice_date as invoice_date,sm_invoice_head.sl as invSl,sm_invoice_head.client_id as client_id,sm_invoice_head.client_name as client_name,sm_invoice_head.area_id as area_id,sm_invoice_head.market_name as market_name,sm_invoice_head.actual_total_tp as actualTpAmt,sm_invoice_head.vat_total_amount as vatTotalAmt,sm_invoice_head.discount as discAmt,sm_invoice_head.sp_discount as spDiscAmt,sm_invoice_head.sp_flat as spFlatDiscAmt,sm_invoice_head.sp_approved as spApprovedDiscAmt,sm_invoice_head.sp_others as spOthersDiscAmt,sm_invoice_head.return_tp as retTpAmt,sm_invoice_head.return_vat as retVatAmt,sm_invoice_head.return_discount as retDiscAmt,sm_invoice_head.return_sp_discount as retSpDiscAmt,sm_invoice_head.discount_precent as discount_precent FROM sm_invoice_head WHERE ("+str(condStr)+") ORDER BY sm_invoice_head.sl"
    else:
        dateRecords=''
        response.flash='Required Date From and Date To'
        
    recordList=db.executesql(dateRecords,as_dict = True)
    invocieCount=len(recordList)
    
    return dict(recordList=recordList,invocieCount=invocieCount,date_from=startDt,date_to=endDt,depot_id=depot_id,depotName=depot_name,store_id=store_id,storeName=store_name,dman_id=dman_id,delivery_man_name=delivery_man_name,territory_id=territory_id,territory_name=territory_name,mso_id=mso_id,mso_name=mso_name,customer_id=customer_id,customerName=customerName,market_id=market_id,market_name=market_name,page=page,items_per_page=items_per_page)    
    
def discount_type_wise_sales_download():
    c_id=session.cid
    
    fromDate=request.vars.date_from
    toDate=request.vars.date_to
    
    depot_id=str(request.vars.depot_id).strip()
    store_id=str(request.vars.store_id).strip()    
    customer_id=str(request.vars.customer_id).strip()
    #customerCat_id=str(request.vars.customerCat_id).strip()
    dman_id=str(request.vars.dman_id).strip()    
    territory_id=str(request.vars.territory_id).strip()  
    market_id=str(request.vars.market_id).strip()
    mso_id=str(request.vars.mso_id).strip()
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
    
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customer_id)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
        
    delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==dman_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        delivery_man_name=dpRow[0].name
        
    territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        territory_name=levelRow[0].level_name
        
    market_name=''
    marketRow=db((db.sm_depot_market.cid==c_id) & (db.sm_depot_market.depot_id==depot_id) & (db.sm_depot_market.market_id==market_id)).select(db.sm_depot_market.market_name,limitby=(0,1))
    if marketRow:
        market_name=marketRow[0].market_name
        
    mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        mso_name=repRow[0].name
    
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
    
    condStr=" (sm_invoice_head.cid = '"+c_id+"') AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.store_id='"+store_id+"') AND ((sm_invoice_head.invoice_date >= '"+str(startDt)+"') AND (sm_invoice_head.invoice_date <= '"+str(endDt)+"')) AND  (sm_invoice_head.status='Invoiced')"
    
    if customer_id!='':
        condStr+=" AND (sm_invoice_head.client_id='"+customer_id+"')"        
    if dman_id!='':
        condStr+=" AND (sm_invoice_head.d_man_id='"+dman_id+"')"        
    if territory_id!='':
        condStr+=" AND (sm_invoice_head.area_id='"+territory_id+"')"      
    if market_id!='':
        condStr+=" AND (sm_invoice_head.market_id='"+market_id+"')"      
    if mso_id!='':
        condStr+=" AND (sm_invoice_head.rep_id='"+mso_id+"')"        
        
    if startDt!='' and endDt!='': 
        dateRecords="SELECT sm_invoice_head.depot_id as depot_id,sm_invoice_head.invoice_date as invoice_date,sm_invoice_head.sl as invSl,sm_invoice_head.client_id as client_id,sm_invoice_head.client_name as client_name,sm_invoice_head.area_id as area_id,sm_invoice_head.market_name as market_name,sm_invoice_head.actual_total_tp as actualTpAmt,sm_invoice_head.regular_disc_tp as regular_disc_tp,sm_invoice_head.flat_disc_tp as flat_disc_tp,sm_invoice_head.approved_disc_tp as approved_disc_tp,sm_invoice_head.others_disc_tp as others_disc_tp,sm_invoice_head.no_disc_tp as no_disc_tp,sm_invoice_head.ret_actual_total_tp as ret_actual_total_tp,sm_invoice_head.ret_regular_disc_tp as ret_regular_disc_tp,sm_invoice_head.ret_flat_disc_tp as ret_flat_disc_tp,sm_invoice_head.ret_approved_disc_tp as ret_approved_disc_tp,sm_invoice_head.ret_others_disc_tp as ret_others_disc_tp,sm_invoice_head.vat_total_amount as vatTotalAmt,sm_invoice_head.discount as discAmt,sm_invoice_head.sp_discount as spDiscAmt,sm_invoice_head.sp_flat as spFlatDiscAmt,sm_invoice_head.sp_approved as spApprovedDiscAmt,sm_invoice_head.sp_others as spOthersDiscAmt,sm_invoice_head.ret_sp_flat as ret_sp_flat,sm_invoice_head.ret_sp_approved as ret_sp_approved,sm_invoice_head.ret_sp_others as ret_sp_others,sm_invoice_head.return_tp as retTpAmt,sm_invoice_head.return_vat as retVatAmt,sm_invoice_head.return_discount as retDiscAmt,sm_invoice_head.return_sp_discount as retSpDiscAmt,sm_invoice_head.discount_precent as discount_precent FROM sm_invoice_head WHERE ("+str(condStr)+") ORDER BY sm_invoice_head.sl"
    else:
        dateRecords=''
        response.flash='Required Date From and Date To'
        
    recordList=db.executesql(dateRecords,as_dict = True)
    invocieCount=len(recordList)
    
    #-------------
    myString='9A Discount Type Wise Sales Statement Details\n'    
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depot_name)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(store_name)+'\n'
    myString+='DP ID:,'+str(dman_id)+'\n'
    myString+='DP Name'+','+str(delivery_man_name)+'\n'
    myString+='Territory ID:,'+str(territory_id)+'\n'
    myString+='Territory Name'+','+str(territory_name)+'\n'
    myString+='MSO ID:,'+str(mso_id)+'\n'
    myString+='MSO Name'+','+str(mso_name)+'\n'
    myString+='Market Name'+','+str(market_name)+'\n'
    myString+='Inv. Date From:,'+str(startDt)+'\n'            
    myString+='Inv.To Date:'+','+str(endDt)+'\n'
    
    myString+=',,,,,,,,,,,Invoice,,,,,,,,,Return,,,,,,,,,Net Sales'+'\n'
    myString+='Inv.Date,Inv.Number,Cust.ID,Cust.Name,MSOTr.,Market Name,Reg. Disc%,Flat Disc%,Approved Disc%,Others Disc%,No Disc TP%,TP,Reg.Disc Amt,Flat Disc Amt,Approved Disc Amt,Others Disc Amt,Total Disc Amt,No Disc TP,VAT,Net,TP,Reg.Disc Amt,Flat Disc Amt,Approved Disc Amt,Others Disc Amt,Total Disc Amt,No Disc TP,VAT,Net,TP,Reg.Disc Amt,Flat Disc Amt,Approved Disc Amt,Others Disc Amt,Total Disc Amt,No Disc TP,VAT,Net \n'
    
    invTpTotal=0
    invDiscTotal=0
    invNetTotal=0
    invVatTotal=0
    
    retTpTotal=0
    retDiscTotal=0
    retNetTotal=0
    retVatTotal=0
    
    invRegDiscTotal=0
    invFlatDiscTotal=0
    invApprovedDiscTotal=0
    invOthersDiscTotal=0
    invNoDiscTotal=0
    
    retRegDiscTotal=0
    retFlatDiscTotal=0
    retApprovedDiscTotal=0
    retOthersDiscTotal=0
    retNoDiscTotal=0
    
    netTpTotal=0
    netDiscTotal=0
    netVatTotal=0
    netGrandTotal=0
    
    net_DiscAmtTotal=0
    net_sp_flatTotal=0
    net_sp_approvedTotal=0
    net_sp_othersTotal=0
    net_no_disc_tpTotal=0
    
    for i in range(len(recordList)):    
        
        recData=recordList[i]
        
        invTpAmt=round(recData['actualTpAmt'],2)
        invTpTotal+=invTpAmt
        invDiscAmt=round(recData['discAmt']+recData['spDiscAmt'],2)
        invDiscTotal+=invDiscAmt
        invVatAmt=round(recData['vatTotalAmt'],2)
        invVatTotal+=invVatAmt
        invNetAmt=round(invTpAmt+invVatAmt-invDiscAmt,2)
        invNetTotal+=invNetAmt
        
        retTpAmt=round(recData['retTpAmt']+recData['retSpDiscAmt'],2)
        retTpTotal+=retTpAmt
        retDiscAmt=round(recData['retDiscAmt']+recData['retSpDiscAmt'],2)
        retDiscTotal+=retDiscAmt
        retVatAmt=round(recData['retVatAmt'],2)
        retVatTotal+=retVatAmt
        retNetAmt=round(retTpAmt+retVatAmt-retDiscAmt,2)
        retNetTotal+=retNetAmt
        
        netTp=invTpAmt-retTpAmt
        netTpTotal+=netTp
        netDisc=invDiscAmt-retDiscAmt
        netDiscTotal+=netDisc
        netVat=invVatAmt-retVatAmt
        netVatTotal+=netVat
        netGrandAmt=invNetAmt-retNetAmt
        netGrandTotal+=netGrandAmt
        
        
        regular_disc_tp=round(recData['regular_disc_tp'],2)
        flat_disc_tp=round(recData['flat_disc_tp'],2)
        approved_disc_tp=round(recData['approved_disc_tp'],2)
        others_disc_tp=round(recData['others_disc_tp'],2)
        no_disc_tp=round(recData['no_disc_tp'],2)
        
        invDiscAmtRD=round(recData['discAmt'],2)
        spFlatDiscAmtSP=round(recData['spFlatDiscAmt'],2)
        spApprovedDiscAmtSP=round(recData['spApprovedDiscAmt'],2)
        spOthersDiscAmtSP=round(recData['spOthersDiscAmt'],2)
        
        invRegDiscTotal+=invDiscAmtRD
        invFlatDiscTotal+=spFlatDiscAmtSP
        invApprovedDiscTotal+=spApprovedDiscAmtSP
        invOthersDiscTotal+=spOthersDiscAmtSP
        invNoDiscTotal+=no_disc_tp
        
        
        discount_precentRD=round(recData['discount_precent'],2)
        
        try:
            regularDiscRate=round((invDiscAmtRD*100)/regular_disc_tp,2)
        except:
            regularDiscRate=0              
        
        #<!--#discount_precentRD=regularDiscRate-->
        
        try:
            spFlatDiscRate=round((spFlatDiscAmtSP*100)/flat_disc_tp,2)
        except:
            spFlatDiscRate=0              
        
        try:
            spApprovedDiscRate=round((spApprovedDiscAmtSP*100)/approved_disc_tp,2)
        except:
            spApprovedDiscRate=0              
        
        try:
            spOthersDiscRate=round((spOthersDiscAmtSP*100)/others_disc_tp,2)
        except:
            spOthersDiscRate=0              
                
        try:
            noDiscRate=round((no_disc_tp*100)/invTpAmt,2)
        except:
            noDiscRate=0
            
        invoice_date=recData['invoice_date']
        invSl=str(session.prefix_invoice)+'INV'+str(recData['depot_id'])+'-'+str(recData['invSl'])
        client_id=recData['client_id']
        client_name=recData['client_name']
        area_id=recData['area_id']
        market_name=recData['market_name']
        
        
        #<!--Return Discount  -->
        ret_actual_total_tp=round(recData['ret_actual_total_tp'],2)
        ret_regular_disc_tp=round(recData['ret_regular_disc_tp'],2)
        ret_flat_disc_tp=round(recData['ret_flat_disc_tp'],2)
        ret_approved_disc_tp=round(recData['ret_approved_disc_tp'],2)
        ret_others_disc_tp=round(recData['ret_others_disc_tp'],2)
        ret_no_disc_tp=round((ret_actual_total_tp-(ret_regular_disc_tp+ret_flat_disc_tp+ret_approved_disc_tp+ret_others_disc_tp)),2)
        
        ret_DiscAmt=round(recData['retDiscAmt'],2)
        ret_sp_flat=round(recData['ret_sp_flat'],2)
        ret_sp_approved=round(recData['ret_sp_approved'],2)
        ret_sp_others=round(recData['ret_sp_others'],2)
        
        retRegDiscTotal+=ret_DiscAmt
        retFlatDiscTotal+=ret_sp_flat
        retApprovedDiscTotal+=ret_sp_approved
        retOthersDiscTotal+=ret_sp_others
        retNoDiscTotal+=ret_no_disc_tp
        
        net_DiscAmt=round(invDiscAmtRD-ret_DiscAmt,2)
        net_sp_flat=round(spFlatDiscAmtSP-ret_sp_flat,2)
        net_sp_approved=round(spApprovedDiscAmtSP-ret_sp_approved,2)
        net_sp_others=round(spOthersDiscAmtSP-ret_sp_others,2)
        net_no_disc_tp=round((no_disc_tp-ret_no_disc_tp),2)
        
        net_DiscAmtTotal+=net_DiscAmt
        net_sp_flatTotal+=net_sp_flat
        net_sp_approvedTotal+=net_sp_approved
        net_sp_othersTotal+=net_sp_others
        net_no_disc_tpTotal+=net_no_disc_tp
        
        #------------------------        
        myString+=str(invoice_date)+','+str(invSl)+','+str(client_id)+','+str(client_name)+','+str(area_id)+','+str(market_name)+','+str(discount_precentRD)+','+\
        str(spFlatDiscRate)+','+str(spApprovedDiscRate)+','+str(spOthersDiscRate)+',0,'+str(invTpAmt)+','+str(invDiscAmtRD)+','+str(spFlatDiscAmtSP)+','+str(spApprovedDiscAmtSP)+','+str(spOthersDiscAmtSP)+','+str(invDiscAmt)+','+str(no_disc_tp)+','+str(invVatAmt)+','+str(invNetAmt)+','+str(retTpAmt)+','+str(ret_DiscAmt)+','+str(ret_sp_flat)+','+str(ret_sp_approved)+','+str(ret_sp_others)+','+str(retDiscAmt)+','+str(ret_no_disc_tp)+','+str(retVatAmt)+','+str(retNetAmt)+','+str(netTp)+','+str(net_DiscAmt)+','+str(net_sp_flat)+','+str(net_sp_approved)+','+str(net_sp_others)+','+str(netDisc)+','+str(net_no_disc_tp)+','+str(netVat)+','+str(netGrandAmt)+'\n'
        
    myString+=str(invocieCount)+' Invoice(s),Total,,,,,,,,,,'+str(round(invTpTotal,2))+','+str(round(invRegDiscTotal,2))+','+str(round(invFlatDiscTotal,2))+','+str(round(invApprovedDiscTotal,2))+','+str(round(invOthersDiscTotal,2))+','+str(round(invDiscTotal,2))+','+str(round(invNoDiscTotal,2))+','+str(round(invVatTotal,2))+','+str(round(invNetTotal,2))+','+str(round(retTpTotal,2))+','+str(round(retRegDiscTotal,2))+','+str(round(retFlatDiscTotal,2))+','+str(round(retApprovedDiscTotal,2))+','+str(round(retOthersDiscTotal,2))+','+str(round(retDiscTotal,2))+','+str(round(retNoDiscTotal,2))+','+str(round(retVatTotal,2))+','+str(round(retNetTotal,2))+','+str(round(netTpTotal,2))+','+str(round(net_DiscAmtTotal,2))+','+str(round(net_sp_flatTotal,2))+','+str(round(net_sp_approvedTotal,2))+','+str(round(net_sp_othersTotal,2))+','+str(round(netDiscTotal,2))+','+str(round(net_no_disc_tpTotal,2))+','+str(round(netVatTotal,2))+','+str(round(netGrandTotal,2))+'\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_discount_typewise_sales.csv'   
    return str(myString)


def discount_type_wise_sales_ad_download():
    c_id=session.cid
    
    fromDate=request.vars.date_from
    toDate=request.vars.date_to
    
    depot_id=str(request.vars.depot_id).strip()
    store_id=str(request.vars.store_id).strip()    
    customer_id=str(request.vars.customer_id).strip()
    #customerCat_id=str(request.vars.customerCat_id).strip()
    dman_id=str(request.vars.dman_id).strip()    
    territory_id=str(request.vars.territory_id).strip()  
    market_id=str(request.vars.market_id).strip()
    mso_id=str(request.vars.mso_id).strip()
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
    
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customer_id)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
        
    delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==dman_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        delivery_man_name=dpRow[0].name
        
    territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        territory_name=levelRow[0].level_name
        
    market_name=''
    marketRow=db((db.sm_depot_market.cid==c_id) & (db.sm_depot_market.depot_id==depot_id) & (db.sm_depot_market.market_id==market_id)).select(db.sm_depot_market.market_name,limitby=(0,1))
    if marketRow:
        market_name=marketRow[0].market_name
        
    mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        mso_name=repRow[0].name
    
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
    
    condStr=" (sm_invoice_head.cid = '"+c_id+"') AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.store_id='"+store_id+"') AND ((sm_invoice_head.invoice_date >= '"+str(startDt)+"') AND (sm_invoice_head.invoice_date <= '"+str(endDt)+"')) AND  (sm_invoice_head.status='Invoiced')"
    
    if customer_id!='':
        condStr+=" AND (sm_invoice_head.client_id='"+customer_id+"')"        
    if dman_id!='':
        condStr+=" AND (sm_invoice_head.d_man_id='"+dman_id+"')"        
    if territory_id!='':
        condStr+=" AND (sm_invoice_head.area_id='"+territory_id+"')"      
    if market_id!='':
        condStr+=" AND (sm_invoice_head.market_id='"+market_id+"')"      
    if mso_id!='':
        condStr+=" AND (sm_invoice_head.rep_id='"+mso_id+"')"        
        
    if startDt!='' and endDt!='': 
        dateRecords="SELECT sm_invoice_head.depot_id as depot_id,sm_invoice_head.invoice_date as invoice_date,sm_invoice_head.sl as invSl,sm_invoice_head.client_id as client_id,sm_invoice_head.client_name as client_name,sm_invoice_head.area_id as area_id,sm_invoice_head.market_name as market_name,sm_invoice_head.actual_total_tp as actualTpAmt,sm_invoice_head.regular_disc_tp as regular_disc_tp,sm_invoice_head.flat_disc_tp as flat_disc_tp,sm_invoice_head.approved_disc_tp as approved_disc_tp,sm_invoice_head.others_disc_tp as others_disc_tp,sm_invoice_head.no_disc_tp as no_disc_tp,sm_invoice_head.ret_actual_total_tp as ret_actual_total_tp,sm_invoice_head.ret_regular_disc_tp as ret_regular_disc_tp,sm_invoice_head.ret_flat_disc_tp as ret_flat_disc_tp,sm_invoice_head.ret_approved_disc_tp as ret_approved_disc_tp,sm_invoice_head.ret_others_disc_tp as ret_others_disc_tp,sm_invoice_head.vat_total_amount as vatTotalAmt,sm_invoice_head.discount as discAmt,sm_invoice_head.sp_discount as spDiscAmt,sm_invoice_head.sp_flat as spFlatDiscAmt,sm_invoice_head.sp_approved as spApprovedDiscAmt,sm_invoice_head.sp_others as spOthersDiscAmt,sm_invoice_head.ret_sp_flat as ret_sp_flat,sm_invoice_head.ret_sp_approved as ret_sp_approved,sm_invoice_head.ret_sp_others as ret_sp_others,sm_invoice_head.return_tp as retTpAmt,sm_invoice_head.return_vat as retVatAmt,sm_invoice_head.return_discount as retDiscAmt,sm_invoice_head.return_sp_discount as retSpDiscAmt,sm_invoice_head.discount_precent as discount_precent FROM sm_invoice_head WHERE ("+str(condStr)+") ORDER BY sm_invoice_head.sl"
    else:
        dateRecords=''
        response.flash='Required Date From and Date To'
        
    recordList=db.executesql(dateRecords,as_dict = True)
    invocieCount=len(recordList)
    
    #-------------
    myString='9B Discount Type Wise Sales Statement (AD)\n'    
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depot_name)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(store_name)+'\n'
    myString+='DP ID:,'+str(dman_id)+'\n'
    myString+='DP Name'+','+str(delivery_man_name)+'\n'
    myString+='Territory ID:,'+str(territory_id)+'\n'
    myString+='Territory Name'+','+str(territory_name)+'\n'
    myString+='MSO ID:,'+str(mso_id)+'\n'
    myString+='MSO Name'+','+str(mso_name)+'\n'
    myString+='Market Name'+','+str(market_name)+'\n'
    myString+='Inv. Date From:,'+str(startDt)+'\n'            
    myString+='Inv.To Date:'+','+str(endDt)+'\n'
    
    myString+=',,,,,,,,,,,Net Sales'+'\n'
    myString+='Inv.Date,Inv.Number,Cust.ID,Cust.Name,MSOTr.,Market Name,Reg. Disc%,Flat Disc%,Approved Disc%,Others Disc%,No Disc TP%,TP,Reg.Disc Amt,Flat Disc Amt,Approved Disc Amt,Others Disc Amt,Total Disc Amt,No Disc TP,VAT,Net \n'
    
    
    invTpTotal=0
    invDiscTotal=0
    invNetTotal=0
    invVatTotal=0
    
    retTpTotal=0
    retDiscTotal=0
    retNetTotal=0
    retVatTotal=0
    
    netTpTotal=0
    netDiscTotal=0
    netVatTotal=0
    netGrandTotal=0
    
    net_DiscAmtTotal=0
    net_sp_flatTotal=0
    net_sp_approvedTotal=0
    net_sp_othersTotal=0
    net_no_disc_tpTotal=0
    
    for i in range(len(recordList)):    
        
        recData=recordList[i]
        
        invTpAmt=round(recData['actualTpAmt'],2)
        invTpTotal+=invTpAmt
        invDiscAmt=round(recData['discAmt']+recData['spDiscAmt'],2)
        invDiscTotal+=invDiscAmt
        invVatAmt=round(recData['vatTotalAmt'],2)
        invVatTotal+=invVatAmt
        invNetAmt=round(invTpAmt+invVatAmt-invDiscAmt,2)
        invNetTotal+=invNetAmt
        
        retTpAmt=round(recData['retTpAmt']+recData['retSpDiscAmt'],2)
        retTpTotal+=retTpAmt
        retDiscAmt=round(recData['retDiscAmt']+recData['retSpDiscAmt'],2)
        retDiscTotal+=retDiscAmt
        retVatAmt=round(recData['retVatAmt'],2)
        retVatTotal+=retVatAmt
        retNetAmt=round(retTpAmt+retVatAmt-retDiscAmt,2)
        retNetTotal+=retNetAmt
        
        netTp=invTpAmt-retTpAmt
        netTpTotal+=netTp
        netDisc=invDiscAmt-retDiscAmt
        netDiscTotal+=netDisc
        netVat=invVatAmt-retVatAmt
        netVatTotal+=netVat
        netGrandAmt=invNetAmt-retNetAmt
        netGrandTotal+=netGrandAmt
        
        
        regular_disc_tp=round(recData['regular_disc_tp'],2)
        flat_disc_tp=round(recData['flat_disc_tp'],2)
        approved_disc_tp=round(recData['approved_disc_tp'],2)
        others_disc_tp=round(recData['others_disc_tp'],2)
        no_disc_tp=round(recData['no_disc_tp'],2)
        
        invDiscAmtRD=round(recData['discAmt'],2)
        spFlatDiscAmtSP=round(recData['spFlatDiscAmt'],2)
        spApprovedDiscAmtSP=round(recData['spApprovedDiscAmt'],2)
        spOthersDiscAmtSP=round(recData['spOthersDiscAmt'],2)
        
        discount_precentRD=round(recData['discount_precent'],2)
        
        try:
            regularDiscRate=round((invDiscAmtRD*100)/regular_disc_tp,2)
        except:
            regularDiscRate=0              
        
        #<!--#discount_precentRD=regularDiscRate-->
        
        try:
            spFlatDiscRate=round((spFlatDiscAmtSP*100)/flat_disc_tp,2)
        except:
            spFlatDiscRate=0              
        
        try:
            spApprovedDiscRate=round((spApprovedDiscAmtSP*100)/approved_disc_tp,2)
        except:
            spApprovedDiscRate=0              
        
        try:
            spOthersDiscRate=round((spOthersDiscAmtSP*100)/others_disc_tp,2)
        except:
            spOthersDiscRate=0              
                
        try:
            noDiscRate=round((no_disc_tp*100)/invTpAmt,2)
        except:
            noDiscRate=0
            
        invoice_date=recData['invoice_date']
        invSl=str(session.prefix_invoice)+'INV'+str(recData['depot_id'])+'-'+str(recData['invSl'])
        client_id=recData['client_id']
        client_name=recData['client_name']
        area_id=recData['area_id']
        market_name=recData['market_name']
        
        
        #<!--Return Discount  -->
        ret_actual_total_tp=round(recData['ret_actual_total_tp'],2)
        ret_regular_disc_tp=round(recData['ret_regular_disc_tp'],2)
        ret_flat_disc_tp=round(recData['ret_flat_disc_tp'],2)
        ret_approved_disc_tp=round(recData['ret_approved_disc_tp'],2)
        ret_others_disc_tp=round(recData['ret_others_disc_tp'],2)
        ret_no_disc_tp=round((ret_actual_total_tp-(ret_regular_disc_tp+ret_flat_disc_tp+ret_approved_disc_tp+ret_others_disc_tp)),2)
        
        ret_DiscAmt=round(recData['retDiscAmt'],2)
        ret_sp_flat=round(recData['ret_sp_flat'],2)
        ret_sp_approved=round(recData['ret_sp_approved'],2)
        ret_sp_others=round(recData['ret_sp_others'],2)
        
        net_DiscAmt=round(invDiscAmtRD-ret_DiscAmt,2)
        net_sp_flat=round(spFlatDiscAmtSP-ret_sp_flat,2)
        net_sp_approved=round(spApprovedDiscAmtSP-ret_sp_approved,2)
        net_sp_others=round(spOthersDiscAmtSP-ret_sp_others,2)
        net_no_disc_tp=round((no_disc_tp-ret_no_disc_tp),2)
        
        net_DiscAmtTotal+=net_DiscAmt
        net_sp_flatTotal+=net_sp_flat
        net_sp_approvedTotal+=net_sp_approved
        net_sp_othersTotal+=net_sp_others
        net_no_disc_tpTotal+=net_no_disc_tp
        
        #------------------------        
        myString+=str(invoice_date)+','+str(invSl)+','+str(client_id)+','+str(client_name)+','+str(area_id)+','+str(market_name)+','+str(discount_precentRD)+','+\
        str(spFlatDiscRate)+','+str(spApprovedDiscRate)+','+str(spOthersDiscRate)+',0,'+str(netTp)+','+str(net_DiscAmt)+','+str(net_sp_flat)+','+str(net_sp_approved)+','+str(net_sp_others)+','+str(netDisc)+','+str(net_no_disc_tp)+','+str(netVat)+','+str(netGrandAmt)+'\n'
        
    myString+=str(invocieCount)+' Invoice(s),Total,,,,,,,,,,'+str(round(netTpTotal,2))+','+str(round(net_DiscAmtTotal,2))+','+str(round(net_sp_flatTotal,2))+','+str(round(net_sp_approvedTotal,2))+','+str(round(net_sp_othersTotal,2))+','+str(round(netDiscTotal,2))+','+str(round(net_no_disc_tpTotal,2))+','+str(round(netVatTotal,2))+','+str(round(netGrandTotal,2))+'\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_discount_typewise_sales_ad.csv'   
    return str(myString)


def discount_type_wise_sales_with_tp_download():
    c_id=session.cid
    
    fromDate=request.vars.date_from
    toDate=request.vars.date_to
    
    depot_id=str(request.vars.depot_id).strip()
    store_id=str(request.vars.store_id).strip()    
    customer_id=str(request.vars.customer_id).strip()
    #customerCat_id=str(request.vars.customerCat_id).strip()
    dman_id=str(request.vars.dman_id).strip()    
    territory_id=str(request.vars.territory_id).strip()  
    market_id=str(request.vars.market_id).strip()
    mso_id=str(request.vars.mso_id).strip()
    discount_type=str(request.vars.discount_type).strip()
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
    
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customer_id)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
        
    delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==dman_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        delivery_man_name=dpRow[0].name
        
    territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        territory_name=levelRow[0].level_name
        
    market_name=''
    marketRow=db((db.sm_depot_market.cid==c_id) & (db.sm_depot_market.depot_id==depot_id) & (db.sm_depot_market.market_id==market_id)).select(db.sm_depot_market.market_name,limitby=(0,1))
    if marketRow:
        market_name=marketRow[0].market_name
        
    mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        mso_name=repRow[0].name
    
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
    
    condStr=" (sm_invoice_head.cid = '"+c_id+"') AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.store_id='"+store_id+"') AND ((sm_invoice_head.invoice_date >= '"+str(startDt)+"') AND (sm_invoice_head.invoice_date <= '"+str(endDt)+"')) AND  (sm_invoice_head.status='Invoiced')"
    
    if customer_id!='':
        condStr+=" AND (sm_invoice_head.client_id='"+customer_id+"')"        
    if dman_id!='':
        condStr+=" AND (sm_invoice_head.d_man_id='"+dman_id+"')"        
    if territory_id!='':
        condStr+=" AND (sm_invoice_head.area_id='"+territory_id+"')"      
    if market_id!='':
        condStr+=" AND (sm_invoice_head.market_id='"+market_id+"')"      
    if mso_id!='':
        condStr+=" AND (sm_invoice_head.rep_id='"+mso_id+"')"        
    
    dateRecords=''
    if discount_type=='REGULAR':
        dateRecords="SELECT sm_invoice_head.depot_id as depot_id,sm_invoice_head.invoice_date as invoice_date,sm_invoice_head.sl as invSl,sm_invoice_head.client_id as client_id,sm_invoice_head.client_name as client_name,sm_invoice_head.area_id as area_id,sm_invoice_head.market_name as market_name,sm_invoice_head.discount_precent as discount_precent,sm_invoice_head.regular_disc_tp as invTp,sm_invoice_head.discount as invDiscAmt,(sm_invoice_head.regular_disc_tp-sm_invoice_head.ret_regular_disc_tp) as tp_amt,(sm_invoice_head.discount-sm_invoice_head.return_discount) as disc_value FROM sm_invoice_head WHERE ("+str(condStr)+" AND (sm_invoice_head.regular_disc_tp-sm_invoice_head.ret_regular_disc_tp)>0) ORDER BY sm_invoice_head.sl"
        
    elif discount_type=='FLAT':
        dateRecords="SELECT sm_invoice_head.depot_id as depot_id,sm_invoice_head.invoice_date as invoice_date,sm_invoice_head.sl as invSl,sm_invoice_head.client_id as client_id,sm_invoice_head.client_name as client_name,sm_invoice_head.area_id as area_id,sm_invoice_head.market_name as market_name,sm_invoice_head.discount_precent as discount_precent,sm_invoice_head.flat_disc_tp as invTp,sm_invoice_head.sp_flat as invDiscAmt,(sm_invoice_head.flat_disc_tp-sm_invoice_head.ret_flat_disc_tp) as tp_amt,(sm_invoice_head.sp_flat-sm_invoice_head.ret_sp_flat) as disc_value FROM sm_invoice_head WHERE ("+str(condStr)+" AND (sm_invoice_head.flat_disc_tp-sm_invoice_head.ret_flat_disc_tp)>0) ORDER BY sm_invoice_head.sl"
        
    elif discount_type=='APPROVED':
        dateRecords="SELECT sm_invoice_head.depot_id as depot_id,sm_invoice_head.invoice_date as invoice_date,sm_invoice_head.sl as invSl,sm_invoice_head.client_id as client_id,sm_invoice_head.client_name as client_name,sm_invoice_head.area_id as area_id,sm_invoice_head.market_name as market_name,sm_invoice_head.discount_precent as discount_precent,sm_invoice_head.approved_disc_tp as invTp,sm_invoice_head.sp_approved as invDiscAmt,(sm_invoice_head.approved_disc_tp-sm_invoice_head.ret_approved_disc_tp) as tp_amt,(sm_invoice_head.sp_approved-sm_invoice_head.ret_sp_approved) as disc_value FROM sm_invoice_head WHERE ("+str(condStr)+" AND (sm_invoice_head.approved_disc_tp-sm_invoice_head.ret_approved_disc_tp)>0) ORDER BY sm_invoice_head.sl"
        
    elif discount_type=='OTHERS':
        dateRecords="SELECT sm_invoice_head.depot_id as depot_id,sm_invoice_head.invoice_date as invoice_date,sm_invoice_head.sl as invSl,sm_invoice_head.client_id as client_id,sm_invoice_head.client_name as client_name,sm_invoice_head.area_id as area_id,sm_invoice_head.market_name as market_name,sm_invoice_head.discount_precent as discount_precent,sm_invoice_head.others_disc_tp as invTp,sm_invoice_head.sp_others as invDiscAmt,(sm_invoice_head.others_disc_tp-sm_invoice_head.ret_others_disc_tp) as tp_amt,(sm_invoice_head.sp_others-sm_invoice_head.ret_sp_others) as disc_value FROM sm_invoice_head WHERE ("+str(condStr)+" AND (sm_invoice_head.others_disc_tp-sm_invoice_head.ret_others_disc_tp)>0) ORDER BY sm_invoice_head.sl"
        
    elif discount_type=='NODISC':
        dateRecords="SELECT sm_invoice_head.depot_id as depot_id,sm_invoice_head.invoice_date as invoice_date,sm_invoice_head.sl as invSl,sm_invoice_head.client_id as client_id,sm_invoice_head.client_name as client_name,sm_invoice_head.area_id as area_id,sm_invoice_head.market_name as market_name,sm_invoice_head.discount_precent as discount_precent,sm_invoice_head.actual_total_tp as invTp,sm_invoice_head.no_disc_tp as invDiscAmt,(sm_invoice_head.no_disc_tp-(sm_invoice_head.ret_actual_total_tp-(sm_invoice_head.ret_regular_disc_tp+sm_invoice_head.ret_flat_disc_tp+sm_invoice_head.ret_approved_disc_tp+sm_invoice_head.ret_others_disc_tp))) as tp_amt,0 as disc_value FROM sm_invoice_head WHERE ("+str(condStr)+" AND (sm_invoice_head.no_disc_tp-(sm_invoice_head.ret_actual_total_tp-(sm_invoice_head.ret_regular_disc_tp+sm_invoice_head.ret_flat_disc_tp+sm_invoice_head.ret_approved_disc_tp+sm_invoice_head.ret_others_disc_tp)))!=0) ORDER BY sm_invoice_head.sl"
        
    recordList=db.executesql(dateRecords,as_dict = True)
    invocieCount=len(recordList)
    
    #-------------
    myString='9C Discount Type Wise Sales Statement With TP (AD)\n'    
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depot_name)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(store_name)+'\n'
    myString+='DP ID:,'+str(dman_id)+'\n'
    myString+='DP Name'+','+str(delivery_man_name)+'\n'
    myString+='Territory ID:,'+str(territory_id)+'\n'
    myString+='Territory Name'+','+str(territory_name)+'\n'
    myString+='MSO ID:,'+str(mso_id)+'\n'
    myString+='MSO Name'+','+str(mso_name)+'\n'
    myString+='Market Name'+','+str(market_name)+'\n'
    myString+='Inv. Date From:,'+str(startDt)+'\n'            
    myString+='Inv.To Date:'+','+str(endDt)+'\n'
    myString+='Discount Type:'+','+str(discount_type)+'\n'
    
    
    myString+='Inv.Date,Inv.Number,Cust.ID,Cust.Name,MSOTr.,Market Name,'+str(discount_type)+' Disc%,Based TP(AD),Disc Amt(AD) \n'
    
    
    netTpTotal=0
    netValueTotal=0
    
    for i in range(len(recordList)):    
        
        recData=recordList[i]
        
        invTp=round(recData['invTp'],2)
        invDiscAmt=round(recData['invDiscAmt'],2)
        discount_precent=0
        if discount_type=='REGULAR':
            discount_precent=round(recData['discount_precent'],2)
        elif discount_type=='FLAT' or discount_type=='APPROVED' or discount_type=='OTHERS': # or discount_type=='NODISC'
            try:
                discount_precent=round((invDiscAmt*100)/invTp,2)
            except:
                discount_precent=0
        
        tp_amt=round(recData['tp_amt'],2)        
        disc_value=round(recData['disc_value'],2)
        
        netTpTotal+=tp_amt
        netValueTotal+=disc_value
            
        invoice_date=recData['invoice_date']
        invSl=str(session.prefix_invoice)+'INV'+str(recData['depot_id'])+'-'+str(recData['invSl'])
        client_id=recData['client_id']
        client_name=recData['client_name']
        area_id=recData['area_id']
        market_name=recData['market_name']
        
        
        #------------------------        
        myString+=str(invoice_date)+','+str(invSl)+','+str(client_id)+','+str(client_name)+','+str(area_id)+','+str(market_name)+','+str(discount_precent)+','+str(tp_amt)+','+str(disc_value)+'\n'
        
    myString+=str(invocieCount)+' Invoice(s),Total,,,,,,'+str(round(netTpTotal,2))+','+str(round(netValueTotal,2))+'\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_discount_typewise_sales_with_tp.csv'   
    return str(myString)


def discount_type_wise_sales_first_download():
    c_id=session.cid
    
    fromDate=request.vars.date_from
    toDate=request.vars.date_to
    
    depot_id=str(request.vars.depot_id).strip()
    store_id=str(request.vars.store_id).strip()    
    customer_id=str(request.vars.customer_id).strip()
    #customerCat_id=str(request.vars.customerCat_id).strip()
    dman_id=str(request.vars.dman_id).strip()    
    territory_id=str(request.vars.territory_id).strip()  
    market_id=str(request.vars.market_id).strip()
    mso_id=str(request.vars.mso_id).strip()
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
    
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customer_id)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
        
    #customerCatName=''
    #clientCatRow=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customerCat_id)).select(db.sm_category_type.cat_type_name,limitby=(0,1))
    #if clientCatRow:
        #customerCatName=clientCatRow[0].cat_type_name
    
    delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==dman_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        delivery_man_name=dpRow[0].name
        
    territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        territory_name=levelRow[0].level_name
        
    market_name=''
    marketRow=db((db.sm_depot_market.cid==c_id) & (db.sm_depot_market.depot_id==depot_id) & (db.sm_depot_market.market_id==market_id)).select(db.sm_depot_market.market_name,limitby=(0,1))
    if marketRow:
        market_name=marketRow[0].market_name
        
    mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        mso_name=repRow[0].name
    
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
    
    condStr=" (sm_invoice_head.cid = '"+c_id+"') AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.store_id='"+store_id+"') AND ((sm_invoice_head.invoice_date >= '"+str(startDt)+"') AND (sm_invoice_head.invoice_date <= '"+str(endDt)+"')) AND  (sm_invoice_head.status='Invoiced')"
    
    if customer_id!='':
        condStr+=" AND (sm_invoice_head.client_id='"+customer_id+"')"        
    if dman_id!='':
        condStr+=" AND (sm_invoice_head.d_man_id='"+dman_id+"')"        
    if territory_id!='':
        condStr+=" AND (sm_invoice_head.area_id='"+territory_id+"')"      
    if market_id!='':
        condStr+=" AND (sm_invoice_head.market_id='"+market_id+"')"      
    if mso_id!='':
        condStr+=" AND (sm_invoice_head.rep_id='"+mso_id+"')"        
        
    if startDt!='' and endDt!='': 
        dateRecords="SELECT sm_invoice_head.depot_id as depot_id,sm_invoice_head.invoice_date as invoice_date,sm_invoice_head.sl as invSl,sm_invoice_head.client_id as client_id,sm_invoice_head.client_name as client_name,sm_invoice_head.area_id as area_id,sm_invoice_head.market_name as market_name,sm_invoice_head.actual_total_tp as actualTpAmt,sm_invoice_head.vat_total_amount as vatTotalAmt,sm_invoice_head.discount as discAmt,sm_invoice_head.sp_discount as spDiscAmt,sm_invoice_head.sp_flat as spFlatDiscAmt,sm_invoice_head.sp_approved as spApprovedDiscAmt,sm_invoice_head.sp_others as spOthersDiscAmt,sm_invoice_head.return_tp as retTpAmt,sm_invoice_head.return_vat as retVatAmt,sm_invoice_head.return_discount as retDiscAmt,sm_invoice_head.return_sp_discount as retSpDiscAmt,sm_invoice_head.discount_precent as discount_precent FROM sm_invoice_head WHERE ("+str(condStr)+") ORDER BY sm_invoice_head.sl"
    else:
        dateRecords=''
        response.flash='Required Date From and Date To'
        
    recordList=db.executesql(dateRecords,as_dict = True)
    invocieCount=len(recordList)
    
    #-------------
    myString='9A Discount Type Wise Sales Statement Details\n'    
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depot_name)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(store_name)+'\n'
    myString+='DP ID:,'+str(dman_id)+'\n'
    myString+='DP Name'+','+str(delivery_man_name)+'\n'
    myString+='Territory ID:,'+str(territory_id)+'\n'
    myString+='Territory Name'+','+str(territory_name)+'\n'
    myString+='MSO ID:,'+str(mso_id)+'\n'
    myString+='MSO Name'+','+str(mso_name)+'\n'
    myString+='Market Name'+','+str(market_name)+'\n'
    myString+='Inv. Date From:,'+str(startDt)+'\n'            
    myString+='Inv.To Date:'+','+str(endDt)+'\n'
    
    myString+=',,,,,,,,,,,Invoice,,,,Return,,,,Net Sales'+'\n'
    myString+='Inv.Date,Inv.Number,Cust.ID,Cust.Name,MSOTr.,Market Name,Reg.Disc%,FlatDisc%,ApprovedDisc%,OthersDisc%,NoDisc%,TP,Disc,VAT,Net,TP,Disc,VAT,Net,TP,Disc,VAT,Net'+'\n'
    
    invTpTotal=0
    invDiscTotal=0
    invNetTotal=0
    invVatTotal=0
    
    retTpTotal=0
    retDiscTotal=0
    retNetTotal=0
    retVatTotal=0
    
    netTpTotal=0
    netDiscTotal=0
    netVatTotal=0
    netGrandTotal=0
    
    for i in range(len(recordList)):    
        
        recData=recordList[i]
        
        invTpAmt=round(recData['actualTpAmt'],2)
        invTpTotal+=invTpAmt
        invDiscAmt=round(recData['discAmt']+recData['spDiscAmt'],2)
        invDiscTotal+=invDiscAmt
        invVatAmt=round(recData['vatTotalAmt'],2)
        invVatTotal+=invVatAmt
        invNetAmt=round(invTpAmt+invVatAmt-invDiscAmt,2)
        invNetTotal+=invNetAmt
        
        retTpAmt=round(recData['retTpAmt']+recData['retSpDiscAmt'],2)
        retTpTotal+=retTpAmt
        retDiscAmt=round(recData['retDiscAmt']+recData['retSpDiscAmt'],2)
        retDiscTotal+=retDiscAmt
        retVatAmt=round(recData['retVatAmt'],2)
        retVatTotal+=retVatAmt
        retNetAmt=round(retTpAmt+retVatAmt-retDiscAmt,2)
        retNetTotal+=retNetAmt
        
        netTp=invTpAmt-retTpAmt
        netTpTotal+=netTp
        netDisc=invDiscAmt-retDiscAmt
        netDiscTotal+=netDisc
        netVat=invVatAmt-retVatAmt
        netVatTotal+=netVat
        netGrandAmt=invNetAmt-retNetAmt
        netGrandTotal+=netGrandAmt
        
        invDiscAmtRD=round(recData['discAmt'],2)
        invDiscAmtSP=round(recData['spDiscAmt'],2)
        spFlatDiscAmtSP=round(recData['spFlatDiscAmt'],2)
        spApprovedDiscAmtSP=round(recData['spApprovedDiscAmt'],2)
        spOthersDiscAmtSP=round(recData['spOthersDiscAmt'],2)
        
        discount_precentRD=round(recData['discount_precent'],2)
        
        try:
            regularDiscRate=round((invDiscAmtRD*100)/invTpAmt,2)
            specialDiscRate=round((invDiscAmtSP*100)/invTpAmt,2)
            spFlatDiscRate=round((spFlatDiscAmtSP*100)/invTpAmt,2)
            spApprovedDiscRate=round((spApprovedDiscAmtSP*100)/invTpAmt,2)
            spOthersDiscRate=round((spOthersDiscAmtSP*100)/invTpAmt,2)            
        except:
            regularDiscRate=0
            specialDiscRate=0      
            spFlatDiscRate=0
            spApprovedDiscRate=0
            spOthersDiscRate=0
        
        noDiscRate=round(100-(regularDiscRate+spFlatDiscRate+spApprovedDiscRate+spOthersDiscRate),2)
         
        invoice_date=recData['invoice_date']
        invSl=str(session.prefix_invoice)+'INV'+str(recData['depot_id'])+'-'+str(recData['invSl'])
        client_id=recData['client_id']
        client_name=recData['client_name']
        area_id=recData['area_id']
        market_name=recData['market_name']
        
        
        #------------------------        
        myString+=str(invoice_date)+','+str(invSl)+','+str(client_id)+','+str(client_name)+','+str(area_id)+','+str(market_name)+','+str(discount_precentRD)+','+\
        str(spFlatDiscRate)+','+str(spApprovedDiscRate)+','+str(spOthersDiscRate)+','+str(noDiscRate)+','+str(invTpAmt)+','+str(invDiscAmt)+','+str(invVatAmt)+','+str(invNetAmt)+','+str(retTpAmt)+','+str(retDiscAmt)+','+str(retVatAmt)+','+str(retNetAmt)+','+str(netTp)+','+str(netDisc)+','+str(netVat)+','+str(netGrandAmt)+'\n'
        
    myString+=str(invocieCount)+' Invoice(s),Total,,,,,,,'+str(round(invTpTotal,2))+','+str(round(invDiscTotal,2))+','+str(round(invVatTotal,2))+','+str(round(invNetTotal,2))+','+str(round(retTpTotal,2))+','+str(round(retDiscTotal,2))+','+str(round(retVatTotal,2))+','+str(round(retNetTotal,2))+','+str(round(netTpTotal,2))+','+str(round(netDiscTotal,2))+','+str(round(netVatTotal,2))+','+str(round(netGrandTotal,2))+'\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_discount_typewise_sales.csv'   
    return str(myString)




def accounting_period_invoice_wise():
    c_id=session.cid
    
    response.title='37 Accounting Period Basis:Invoice wise'
    
    fromDate=request.vars.date_from
    toDate=request.vars.date_to
    
    depot_id=str(request.vars.depot_id).strip()
    store_id=str(request.vars.store_id).strip()    
    customer_id=str(request.vars.customer_id).strip()
    #customerCat_id=str(request.vars.customerCat_id).strip()
    dman_id=str(request.vars.dman_id).strip()    
    territory_id=str(request.vars.teritory_id).strip()  
    market_id=str(request.vars.market_id).strip()
    mso_id=str(request.vars.mso_id).strip()
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
    
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customer_id)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
        
    #customerCatName=''
    #clientCatRow=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customerCat_id)).select(db.sm_category_type.cat_type_name,limitby=(0,1))
    #if clientCatRow:
        #customerCatName=clientCatRow[0].cat_type_name
    
    delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==dman_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        delivery_man_name=dpRow[0].name
        
    territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        territory_name=levelRow[0].level_name
        
    market_name=''
    marketRow=db((db.sm_depot_market.cid==c_id) & (db.sm_depot_market.depot_id==depot_id) & (db.sm_depot_market.market_id==market_id)).select(db.sm_depot_market.market_name,limitby=(0,1))
    if marketRow:
        market_name=marketRow[0].market_name
        
    mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        mso_name=repRow[0].name
    
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
    
    condStr1=" (sm_invoice_head.cid = '"+c_id+"') AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.store_id='"+store_id+"') AND ((sm_invoice_head.invoice_date >= '"+str(startDt)+"') AND (sm_invoice_head.invoice_date <= '"+str(endDt)+"')) AND (sm_invoice_head.status='Invoiced')"
    
    condStr2=" (sm_return_head.cid = '"+c_id+"') AND (sm_return_head.depot_id='"+depot_id+"') AND (sm_return_head.store_id='"+store_id+"') AND ((sm_return_head.return_date >= '"+str(startDt)+"') AND (sm_return_head.return_date <= '"+str(endDt)+"')) AND (sm_return_head.status='Returned')"
    
    if customer_id!='':
        condStr1+=" AND (sm_invoice_head.client_id='"+customer_id+"')"
        condStr2+=" AND (sm_return_head.client_id='"+customer_id+"')"        
    if dman_id!='':
        condStr1+=" AND (sm_invoice_head.d_man_id='"+dman_id+"')"     
        condStr2+=" AND (sm_return_head.d_man_id='"+dman_id+"')"   
    if territory_id!='':
        condStr1+=" AND (sm_invoice_head.area_id='"+territory_id+"')"
        condStr2+=" AND (sm_return_head.area_id='"+territory_id+"')"       
    if market_id!='':
        condStr1+=" AND (sm_invoice_head.market_id='"+market_id+"')"
        condStr2+=" AND (sm_return_head.market_id='"+market_id+"')"      
    if mso_id!='':
        condStr1+=" AND (sm_invoice_head.rep_id='"+mso_id+"')" 
        condStr2+=" AND (sm_return_head.rep_id='"+mso_id+"')"       
        
    if startDt!='' and endDt!='': 
        dateRecords1="SELECT sm_invoice_head.depot_id as depot_id,sm_invoice_head.sl as invSl,sm_invoice_head.invoice_date as invoice_date,sm_invoice_head.shipment_no as shipment_no,sm_invoice_head.client_name as client_name,sm_invoice_head.actual_total_tp as actualTpAmt,sm_invoice_head.vat_total_amount as vatTotalAmt,sm_invoice_head.discount as discAmt,sm_invoice_head.sp_discount as spDiscAmt,0 as retTpAmt,0 as retVatAmt,0 as retDiscAmt,0 as retSpDiscAmt FROM sm_invoice_head WHERE ( "+str(condStr1)+") ORDER BY sm_invoice_head.sl"
        dateRecords2="SELECT sm_return_head.depot_id as depot_id,sm_return_head.invoice_sl as invSl,sm_return_head.invoice_date as invoice_date,sm_return_head.shipment_no as shipment_no,sm_return_head.client_name as client_name,0 as actualTpAmt,0 as vatTotalAmt,0 as discAmt,0 as spDiscAmt,SUM((sm_return_head.total_amount-sm_return_head.vat_total_amount+sm_return_head.discount)+sm_return_head.sp_discount) as retTpAmt,SUM(sm_return_head.vat_total_amount) as retVatAmt,SUM(sm_return_head.discount) as retDiscAmt,SUM(sm_return_head.sp_discount) as retSpDiscAmt FROM sm_return_head WHERE ( "+str(condStr2)+") GROUP BY sm_return_head.depot_id,sm_return_head.invoice_sl,sm_return_head.invoice_date,sm_return_head.shipment_no,sm_return_head.client_name ORDER BY sm_return_head.invoice_sl"
    else:
        dateRecords1=''
        dateRecords2=''
        response.flash='Required Date From and Date To'
        
    recordList1=db.executesql(dateRecords1,as_dict = True)
    recordList2=db.executesql(dateRecords2,as_dict = True)
        
    recordList=[]
    
    for i in range(len(recordList1)):
        invDict=recordList1[i]
        inv_sl=invDict['invSl']
        
        ret_index=-1
        try:
            ret_index=str(map(itemgetter('invSl'), recordList2).index(inv_sl))    
        except:
            ret_index=-1
            
        if (ret_index!=-1):
            retDictData=recordList2[int(ret_index)]
            
            invDict['retTpAmt']=str(retDictData['retTpAmt'])
            invDict['retVatAmt']=str(retDictData['retVatAmt'])
            invDict['retDiscAmt']=str(retDictData['retDiscAmt'])
            
            #recordList2.pop(ret_index)
            del recordList2[int(ret_index)]
    
    recordList=recordList1+recordList2
    
    recordList.sort(key=itemgetter('invSl'), reverse=False)
    
    return dict(recordList=recordList,date_from=startDt,date_to=endDt,depot_id=depot_id,depotName=depot_name,store_id=store_id,storeName=store_name,dman_id=dman_id,delivery_man_name=delivery_man_name,territory_id=territory_id,territory_name=territory_name,mso_id=mso_id,mso_name=mso_name,customer_id=customer_id,customerName=customerName,market_id=market_id,market_name=market_name,page=page,items_per_page=items_per_page)    



def customer_type_wise_sales():
    c_id=session.cid
    
    response.title='20. Customer Type Wise Sales Details'
    
    fromDate=request.vars.date_from
    toDate=request.vars.date_to
    
    depot_id=str(request.vars.depot_id).strip()
    store_id=str(request.vars.store_id).strip()    
    customer_id=str(request.vars.customer_id).strip()
    #customerCat_id=str(request.vars.customerCat_id).strip()
    dman_id=str(request.vars.dman_id).strip()    
    territory_id=str(request.vars.teritory_id).strip()  
    market_id=str(request.vars.market_id).strip()
    mso_id=str(request.vars.mso_id).strip()
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
    
    customerName=''
    clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.depot_id==depot_id)&(db.sm_client.client_id==customer_id)).select(db.sm_client.name,limitby=(0,1))
    if clientRow:
        customerName=clientRow[0].name
        
    #customerCatName=''
    #clientCatRow=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')&(db.sm_category_type.cat_type_id==customerCat_id)).select(db.sm_category_type.cat_type_name,limitby=(0,1))
    #if clientCatRow:
        #customerCatName=clientCatRow[0].cat_type_name
    
    delivery_man_name=''
    dpRow=db((db.sm_delivery_man.cid==c_id)&(db.sm_delivery_man.depot_id==depot_id)&(db.sm_delivery_man.d_man_id==dman_id)).select(db.sm_delivery_man.name,limitby=(0,1))
    if dpRow:
        delivery_man_name=dpRow[0].name
        
    territory_name=''
    levelRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id)).select(db.sm_level.level_name,limitby=(0,1))
    if levelRow:
        territory_name=levelRow[0].level_name
        
    market_name=''
    marketRow=db((db.sm_depot_market.cid==c_id) & (db.sm_depot_market.depot_id==depot_id) & (db.sm_depot_market.market_id==market_id)).select(db.sm_depot_market.market_name,limitby=(0,1))
    if marketRow:
        market_name=marketRow[0].market_name
        
    mso_name=''
    repRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==mso_id)).select(db.sm_rep.name,limitby=(0,1))
    if repRow:
        mso_name=repRow[0].name
    
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
    
    condStr1=" (sm_invoice_head.cid = '"+c_id+"') AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.store_id='"+store_id+"') AND ((sm_invoice_head.invoice_date >= '"+str(startDt)+"') AND (sm_invoice_head.invoice_date <= '"+str(endDt)+"')) AND (sm_invoice_head.status='Invoiced')"
    
    condStr2=" (sm_return_head.cid = '"+c_id+"') AND (sm_return_head.depot_id='"+depot_id+"') AND (sm_return_head.store_id='"+store_id+"') AND ((sm_return_head.return_date >= '"+str(startDt)+"') AND (sm_return_head.return_date <= '"+str(endDt)+"')) AND (sm_return_head.status='Returned')"
    
    if customer_id!='':
        condStr1+=" AND (sm_invoice_head.client_id='"+customer_id+"')"
        condStr2+=" AND (sm_return_head.client_id='"+customer_id+"')"        
    if dman_id!='':
        condStr1+=" AND (sm_invoice_head.d_man_id='"+dman_id+"')"     
        condStr2+=" AND (sm_return_head.d_man_id='"+dman_id+"')"   
    if territory_id!='':
        condStr1+=" AND (sm_invoice_head.area_id='"+territory_id+"')"
        condStr2+=" AND (sm_return_head.area_id='"+territory_id+"')"       
    if market_id!='':
        condStr1+=" AND (sm_invoice_head.market_id='"+market_id+"')"
        condStr2+=" AND (sm_return_head.market_id='"+market_id+"')"      
    if mso_id!='':
        condStr1+=" AND (sm_invoice_head.rep_id='"+mso_id+"')" 
        condStr2+=" AND (sm_return_head.rep_id='"+mso_id+"')"       
        
    if startDt!='' and endDt!='':
        dateRecords1="SELECT sm_invoice_head.depot_id as depot_id,sm_invoice_head.sl as invSl,sm_invoice_head.invoice_date as invoice_date,sm_invoice_head.client_id as client_id,sm_invoice_head.client_name as client_name,sm_invoice_head.cl_category_name as cl_category_name,sm_invoice_head.actual_total_tp as actualTpAmt,sm_invoice_head.vat_total_amount as vatTotalAmt,sm_invoice_head.discount as discAmt,sm_invoice_head.sp_discount as spDiscAmt,0 as retTpAmt,0 as retVatAmt,0 as retDiscAmt,0 as retSpDiscAmt FROM sm_invoice_head WHERE ( "+str(condStr1)+") ORDER BY sm_invoice_head.sl"
        dateRecords2="SELECT sm_return_head.depot_id as depot_id,sm_return_head.invoice_sl as invSl,sm_return_head.invoice_date as invoice_date,sm_return_head.client_id as client_id,MAX(sm_return_head.client_name) as client_name,MAX(sm_return_head.cl_category_name) as cl_category_name,0 as actualTpAmt,0 as vatTotalAmt,0 as discAmt,0 as spDiscAmt,SUM((sm_return_head.total_amount-sm_return_head.vat_total_amount+sm_return_head.discount)+sm_return_head.sp_discount) as retTpAmt,SUM(sm_return_head.vat_total_amount) as retVatAmt,SUM(sm_return_head.discount) as retDiscAmt,SUM(sm_return_head.sp_discount) as retSpDiscAmt FROM sm_return_head WHERE ( "+str(condStr2)+") GROUP BY sm_return_head.depot_id,sm_return_head.invoice_sl,sm_return_head.invoice_date,sm_return_head.client_id ORDER BY sm_return_head.invoice_sl"
    else:
        dateRecords1=''
        dateRecords2=''
        response.flash='Required Date From and Date To'
        
    recordList1=db.executesql(dateRecords1,as_dict = True)
    recordList2=db.executesql(dateRecords2,as_dict = True)
    
    recordList=[]
    
    for i in range(len(recordList1)):
        invDict=recordList1[i]
        inv_sl=invDict['invSl']
        
        ret_index=-1
        try:
            ret_index=str(map(itemgetter('invSl'), recordList2).index(inv_sl))    
        except:
            ret_index=-1
            
        if (ret_index!=-1):
            retDictData=recordList2[int(ret_index)]
            
            invDict['retTpAmt']=str(retDictData['retTpAmt'])
            invDict['retVatAmt']=str(retDictData['retVatAmt'])
            invDict['retDiscAmt']=str(retDictData['retDiscAmt'])
            
            #recordList2.pop(ret_index)
            del recordList2[int(ret_index)]
    
    recordList=recordList1+recordList2
    
    recordList.sort(key=itemgetter('invSl'), reverse=False)
    
    return dict(recordList=recordList,date_from=startDt,date_to=endDt,depot_id=depot_id,depotName=depot_name,store_id=store_id,storeName=store_name,dman_id=dman_id,delivery_man_name=delivery_man_name,territory_id=territory_id,territory_name=territory_name,mso_id=mso_id,mso_name=mso_name,customer_id=customer_id,customerName=customerName,market_id=market_id,market_name=market_name,page=page,items_per_page=items_per_page)    


def sales_vat_discount_reconciliation():
    c_id=session.cid
    
    response.title='38. Sales VAT Discount Reconciliation Statement'
    
    fromDate=request.vars.date_from
    toDate=request.vars.date_to
    
    depot_id=str(request.vars.depot_id).strip()
    store_id=str(request.vars.store_id).strip()    
        
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    try:        
        startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        startDt=''                
        
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    currentMonth=str(toDate)[0:7] + '-01'
    currentMonthDate = datetime.datetime.strptime(str(currentMonth), '%Y-%m-%d')
    last_1_monthDate = sub_months(currentMonthDate, 1)#.strftime('%Y-%m-%d')
        
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    #------------------ Total Collection
    transactionCause="'','COLLECTION ERROR','ENTRY ERROR'"    #AND (sm_payment_collection.store_id='"+store_id+"') 
    condStr1=" (sm_payment_collection.cid = '"+c_id+"') AND (sm_payment_collection.depot_id='"+depot_id+"') AND (sm_payment_collection.payment_ym_date = '"+str(currentMonth)+"') AND (sm_payment_collection.status='Posted') AND (sm_payment_collection.transaction_cause IN ("+str(transactionCause)+"))"
    paymentRecords1="(SELECT sm_payment_collection.head_rowid as hRowId,ROUND(SUM(sm_payment_collection.collection_amount),2) as collAmt FROM sm_payment_collection WHERE ("+str(condStr1)+") GROUP BY sm_payment_collection.head_rowid ORDER BY sm_payment_collection.head_rowid)"
    
    records1="SELECT sm_invoice_head.depot_id as depot_id,SUM(sm_invoice_head.actual_total_tp) as actualTpAmt,SUM(sm_invoice_head.vat_total_amount) as vatTotalAmt,SUM(sm_invoice_head.discount) as discAmt,SUM(sm_invoice_head.sp_discount) as spDiscAmt,SUM(sm_invoice_head.adjust_amount) as adjustAmt,SUM(sm_invoice_head.return_tp) as retTpAmt,SUM(sm_invoice_head.return_vat) as retVatAmt,SUM(sm_invoice_head.return_discount) as retDiscAmt,SUM(sm_invoice_head.return_sp_discount) as retSpDiscAmt,SUM(smPay.collAmt) as collAmt FROM sm_invoice_head,"+str(paymentRecords1)+" as smPay WHERE ((sm_invoice_head.cid = '"+c_id+"') AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.id=smPay.hRowId) ) GROUP BY sm_invoice_head.depot_id"
    recordList1=db.executesql(records1,as_dict = True)
    
    collectionTp=0
    collectionVat=0
    collectionDisc=0
    for i in range(len(recordList1)):
        actualTpAmt=float(recordList1[i]['actualTpAmt'])
        vatTotalAmt=float(recordList1[i]['vatTotalAmt'])
        discAmt=float(recordList1[i]['discAmt'])
        spDiscAmt=float(recordList1[i]['spDiscAmt'])
        
        retTpAmt=float(recordList1[i]['retTpAmt'])
        retVatAmt=float(recordList1[i]['retVatAmt'])
        retDiscAmt=float(recordList1[i]['retDiscAmt'])
        retSpDiscAmt=float(recordList1[i]['retSpDiscAmt'])
        
        invTp=round(actualTpAmt,2)#-(retTpAmt+retSpDiscAmt) 
        invVat=round(vatTotalAmt,2)#-retVatAmt
        invDiscount=round(discAmt,2)#-retDiscAmt
        invSpDisc=round(spDiscAmt,2)#-retSpDiscAmt
        
        invNetAmt=round(invTp+invVat-(invDiscount+invSpDisc),2)
        
        collection=round(recordList1[i]['collAmt'],2)#invNetAmt-
        try:
            collTp=(invTp*collection)/invNetAmt
            collVat=(invVat*collection)/invNetAmt
            collDisc=(invDiscount*collection)/invNetAmt
            collSp=(invSpDisc*collection)/invNetAmt
            
            collectionTp=collTp
            collectionVat=collVat
            collectionDisc=collDisc+collSp
        except:
            pass
        break
    
    #------------------ Credit Sale Outstanding #AND (sm_invoice_head.store_id='"+store_id+"')
    condStr2="(sm_invoice_head.cid = '"+c_id+"') AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.invoice_ym_date = '"+str(currentMonth)+"') AND (sm_invoice_head.status='Invoiced')"
    condStr2+=" AND (round(sm_invoice_head.total_amount-(sm_invoice_head.return_tp+sm_invoice_head.return_vat-sm_invoice_head.return_discount)-sm_invoice_head.collection_amount,2)!=0)"
    condStr2+=" AND (sm_invoice_head.payment_mode='CREDIT')"    
    records2="SELECT sm_invoice_head.depot_id as depot_id,SUM(sm_invoice_head.actual_total_tp) as actualTpAmt,SUM(sm_invoice_head.vat_total_amount) as vatTotalAmt,SUM(sm_invoice_head.discount) as discAmt,SUM(sm_invoice_head.sp_discount) as spDiscAmt,SUM(sm_invoice_head.adjust_amount) as adjustAmt,SUM(sm_invoice_head.return_tp) as retTpAmt,SUM(sm_invoice_head.return_vat) as retVatAmt,SUM(sm_invoice_head.return_discount) as retDiscAmt,SUM(sm_invoice_head.return_sp_discount) as retSpDiscAmt,SUM(sm_invoice_head.collection_amount) as collAmt FROM sm_invoice_head WHERE ("+str(condStr2)+") GROUP BY sm_invoice_head.depot_id"
    recordList2=db.executesql(records2,as_dict = True)
    
    creditTpOst=0
    creditVatOst=0
    creditDiscOst=0
    for j in range(len(recordList2)):
        actualTpAmt=float(recordList2[j]['actualTpAmt'])
        vatTotalAmt=float(recordList2[j]['vatTotalAmt'])
        discAmt=float(recordList2[j]['discAmt'])
        spDiscAmt=float(recordList2[j]['spDiscAmt'])
        
        retTpAmt=float(recordList2[j]['retTpAmt'])
        retVatAmt=float(recordList2[j]['retVatAmt'])
        retDiscAmt=float(recordList2[j]['retDiscAmt'])
        retSpDiscAmt=float(recordList2[j]['retSpDiscAmt'])
        
        invTp=round(actualTpAmt-(retTpAmt+retSpDiscAmt),2)
        invVat=round(vatTotalAmt-retVatAmt,2)
        invDiscount=round(discAmt-retDiscAmt,2)
        invSpDisc=round(spDiscAmt-retSpDiscAmt,2)
        
        invNetAmt=round(invTp+invVat-(invDiscount+invSpDisc),2)
        
        outstanding=round(invNetAmt-recordList2[j]['collAmt'],2)
        try:
            outTp=(invTp*outstanding)/invNetAmt
            outVat=(invVat*outstanding)/invNetAmt
            outDisc=(invDiscount*outstanding)/invNetAmt
            outSp=(invSpDisc*outstanding)/invNetAmt
            
            creditTpOst=outTp
            creditVatOst=outVat
            creditDiscOst=outDisc+outSp
        except:
            pass
        break
    
    #------------------------- Cash Sale Outstanding    #AND (sm_invoice_head.store_id='"+store_id+"')
    condStr3="(sm_invoice_head.cid = '"+c_id+"') AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.invoice_ym_date = '"+str(currentMonth)+"') AND (sm_invoice_head.status='Invoiced')"
    condStr3+=" AND (round(sm_invoice_head.total_amount-(sm_invoice_head.return_tp+sm_invoice_head.return_vat-sm_invoice_head.return_discount)-sm_invoice_head.collection_amount,2)!=0)"
    condStr3+=" AND (sm_invoice_head.payment_mode='CASH')"    
    records3="SELECT sm_invoice_head.depot_id as depot_id,SUM(sm_invoice_head.actual_total_tp) as actualTpAmt,SUM(sm_invoice_head.vat_total_amount) as vatTotalAmt,SUM(sm_invoice_head.discount) as discAmt,SUM(sm_invoice_head.sp_discount) as spDiscAmt,SUM(sm_invoice_head.adjust_amount) as adjustAmt,SUM(sm_invoice_head.return_tp) as retTpAmt,SUM(sm_invoice_head.return_vat) as retVatAmt,SUM(sm_invoice_head.return_discount) as retDiscAmt,SUM(sm_invoice_head.return_sp_discount) as retSpDiscAmt,SUM(sm_invoice_head.collection_amount) as collAmt FROM sm_invoice_head WHERE ("+str(condStr3)+") GROUP BY sm_invoice_head.depot_id"
    recordList3=db.executesql(records3,as_dict = True)
    
    cashTpOst=0
    cashVatOst=0
    cashDiscOst=0
    for k in range(len(recordList3)):
        actualTpAmt=float(recordList3[k]['actualTpAmt'])
        vatTotalAmt=float(recordList3[k]['vatTotalAmt'])
        discAmt=float(recordList3[k]['discAmt'])
        spDiscAmt=float(recordList3[k]['spDiscAmt'])
        
        retTpAmt=float(recordList3[k]['retTpAmt'])
        retVatAmt=float(recordList3[k]['retVatAmt'])
        retDiscAmt=float(recordList3[k]['retDiscAmt'])
        retSpDiscAmt=float(recordList3[k]['retSpDiscAmt'])
        
        invTp=round(actualTpAmt-(retTpAmt+retSpDiscAmt),2)
        invVat=round(vatTotalAmt-retVatAmt,2)
        invDiscount=round(discAmt-retDiscAmt,2)
        invSpDisc=round(spDiscAmt-retSpDiscAmt,2)
        
        invNetAmt=round(invTp+invVat-(invDiscount+invSpDisc),2)
        
        outstanding=round(invNetAmt-recordList3[k]['collAmt'],2)
        try:
            outTp=(invTp*outstanding)/invNetAmt
            outVat=(invVat*outstanding)/invNetAmt
            outDisc=(invDiscount*outstanding)/invNetAmt
            outSp=(invSpDisc*outstanding)/invNetAmt
            
            cashTpOst=outTp
            cashVatOst=outVat
            cashDiscOst=outDisc+outSp
        except:
            pass
        break
    
    #---------------------- Collection this month but previous outstanding
    transactionCause="'','COLLECTION ERROR','ENTRY ERROR'"    # AND (sm_payment_collection.store_id='"+store_id+"')
    condStr4=" (sm_payment_collection.cid = '"+c_id+"') AND (sm_payment_collection.depot_id='"+depot_id+"') AND (sm_payment_collection.payment_ym_date = '"+str(currentMonth)+"') AND (sm_payment_collection.status='Posted') AND (sm_payment_collection.transaction_cause IN ("+str(transactionCause)+"))"
    paymentRecords4="(SELECT sm_payment_collection.head_rowid as hRowId,ROUND(SUM(sm_payment_collection.collection_amount),2) as collAmt FROM sm_payment_collection WHERE ("+str(condStr4)+") GROUP BY sm_payment_collection.head_rowid ORDER BY sm_payment_collection.head_rowid)"
    
    records4="SELECT sm_invoice_head.depot_id as depot_id,SUM(sm_invoice_head.actual_total_tp) as actualTpAmt,SUM(sm_invoice_head.vat_total_amount) as vatTotalAmt,SUM(sm_invoice_head.discount) as discAmt,SUM(sm_invoice_head.sp_discount) as spDiscAmt,SUM(sm_invoice_head.adjust_amount) as adjustAmt,SUM(sm_invoice_head.return_tp) as retTpAmt,SUM(sm_invoice_head.return_vat) as retVatAmt,SUM(sm_invoice_head.return_discount) as retDiscAmt,SUM(sm_invoice_head.return_sp_discount) as retSpDiscAmt,SUM(smPay.collAmt) as collAmt FROM sm_invoice_head,"+str(paymentRecords4)+" as smPay WHERE ((sm_invoice_head.cid = '"+c_id+"') AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.payment_mode='CREDIT') AND (sm_invoice_head.invoice_ym_date<='"+str(last_1_monthDate)+"') AND (sm_invoice_head.id=smPay.hRowId)) GROUP BY sm_invoice_head.depot_id"
    recordList4=db.executesql(records4,as_dict = True)
    
    realisedTp=0
    realisedVat=0
    realisedDisc=0
    for m in range(len(recordList4)):
        actualTpAmt=float(recordList4[m]['actualTpAmt'])
        vatTotalAmt=float(recordList4[m]['vatTotalAmt'])
        discAmt=float(recordList4[m]['discAmt'])
        spDiscAmt=float(recordList4[m]['spDiscAmt'])
        
        retTpAmt=float(recordList4[m]['retTpAmt'])
        retVatAmt=float(recordList4[m]['retVatAmt'])
        retDiscAmt=float(recordList4[m]['retDiscAmt'])
        retSpDiscAmt=float(recordList4[m]['retSpDiscAmt'])
        
        invTp=round(actualTpAmt,2)#-(retTpAmt+retSpDiscAmt) 
        invVat=round(vatTotalAmt,2)#-retVatAmt
        invDiscount=round(discAmt,2)#-retDiscAmt
        invSpDisc=round(spDiscAmt,2)#-retSpDiscAmt
        
        invNetAmt=round(invTp+invVat-(invDiscount+invSpDisc),2)
        
        collection=round(recordList4[m]['collAmt'],2)#invNetAmt-
        try:
            collTp=(invTp*collection)/invNetAmt
            collVat=(invVat*collection)/invNetAmt
            collDisc=(invDiscount*collection)/invNetAmt
            collSp=(invSpDisc*collection)/invNetAmt
            
            realisedTp=collTp
            realisedVat=collVat
            realisedDisc=collDisc+collSp
        except:
            pass
        break
    
    #---------------------- Return this month but invoice previous #AND (sm_return_head.store_id='"+store_id+"') 
    condStr5=" (sm_return_head.cid = '"+c_id+"') AND (sm_return_head.depot_id='"+depot_id+"') AND (sm_return_head.ym_date = '"+str(currentMonth)+"') AND (sm_return_head.invoice_ym_date<='"+str(last_1_monthDate)+"')  AND (sm_return_head.status='Returned')"
    records5="SELECT sm_return_head.depot_id as depot_id,SUM((sm_return_head.total_amount-sm_return_head.vat_total_amount+sm_return_head.discount)+sm_return_head.sp_discount) as retTpAmt,SUM(sm_return_head.vat_total_amount) as retVatAmt,SUM(sm_return_head.discount) as retDiscAmt,SUM(sm_return_head.sp_discount) as retSpDiscAmt FROM sm_return_head WHERE ( "+str(condStr5)+") GROUP BY sm_return_head.depot_id"
    recordList5=db.executesql(records5,as_dict = True)
    
    prevRetTp=0
    prevRetVat=0
    prevRetDisc=0
    for n in range(len(recordList5)):        
        retTpAmt=float(recordList5[n]['retTpAmt'])
        retVatAmt=float(recordList5[n]['retVatAmt'])
        retDiscAmt=float(recordList5[n]['retDiscAmt'])
        retSpDiscAmt=float(recordList5[n]['retSpDiscAmt'])
        prevRetTp=round(retTpAmt,2)
        prevRetVat=round(retVatAmt,2)
        prevRetDisc=round(retDiscAmt+retSpDiscAmt,2)        
        break
    
    
    
    #------------------------- Net Sale     #AND (sm_invoice_head.store_id='"+store_id+"')
    condStr6="(sm_invoice_head.cid = '"+c_id+"') AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.invoice_ym_date = '"+str(currentMonth)+"') AND (sm_invoice_head.status='Invoiced')"
    
    records6="SELECT sm_invoice_head.depot_id as depot_id,SUM(sm_invoice_head.actual_total_tp) as actualTpAmt,SUM(sm_invoice_head.vat_total_amount) as vatTotalAmt,SUM(sm_invoice_head.discount) as discAmt,SUM(sm_invoice_head.sp_discount) as spDiscAmt,SUM(sm_invoice_head.adjust_amount) as adjustAmt,SUM(sm_invoice_head.return_tp) as retTpAmt,SUM(sm_invoice_head.return_vat) as retVatAmt,SUM(sm_invoice_head.return_discount) as retDiscAmt,SUM(sm_invoice_head.return_sp_discount) as retSpDiscAmt FROM sm_invoice_head WHERE ("+str(condStr6)+") GROUP BY sm_invoice_head.depot_id"
    recordList6=db.executesql(records6,as_dict = True)
    
    salesTp=0
    salesVat=0
    salesDisc=0
    for p in range(len(recordList6)):
        actualTpAmt=float(recordList6[p]['actualTpAmt'])
        vatTotalAmt=float(recordList6[p]['vatTotalAmt'])
        discAmt=float(recordList6[p]['discAmt'])
        spDiscAmt=float(recordList6[p]['spDiscAmt'])
        
        retTpAmt=float(recordList6[p]['retTpAmt'])
        retVatAmt=float(recordList6[p]['retVatAmt'])
        retDiscAmt=float(recordList6[p]['retDiscAmt'])
        retSpDiscAmt=float(recordList6[p]['retSpDiscAmt'])
        
        invTp=round(actualTpAmt-(retTpAmt+retSpDiscAmt),2)
        invVat=round(vatTotalAmt-retVatAmt,2)
        invDiscount=round(discAmt-retDiscAmt,2)
        invSpDisc=round(spDiscAmt-retSpDiscAmt,2)
        
        salesTp=invTp
        salesVat=invVat
        salesDisc=invDiscount+invSpDisc
                
        break
        
    return dict(collectionTp=collectionTp,collectionVat=collectionVat,collectionDisc=collectionDisc,creditTpOst=creditTpOst,creditVatOst=creditVatOst,creditDiscOst=creditDiscOst,cashTpOst=cashTpOst,cashVatOst=cashVatOst,cashDiscOst=cashDiscOst,realisedTp=realisedTp,realisedVat=realisedVat,realisedDisc=realisedDisc,prevRetTp=prevRetTp,prevRetVat=prevRetVat,prevRetDisc=prevRetDisc,salesTp=salesTp,salesVat=salesVat,salesDisc=salesDisc,date_from=startDt,date_to=endDt,currentMonthDate=currentMonthDate,depot_id=depot_id,depotName=depot_name,store_id=store_id,storeName=store_name,page=page,items_per_page=items_per_page)    
    
def ar_reconciliation():
    c_id=session.cid
    
    response.title='39. A/R Reconciliation Statement'
    
    fromDate=request.vars.date_from
    toDate=request.vars.date_to
    
    depot_id=str(request.vars.depot_id).strip()
    store_id=str(request.vars.store_id).strip()    
        
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
    if storeRow:
        store_name=storeRow[0].store_name
        
    try:        
        startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        startDt=''                
        
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    currentMonth=str(toDate)[0:7] + '-01'
    currentMonthDate = datetime.datetime.strptime(str(currentMonth), '%Y-%m-%d')
    last_1_monthDate = sub_months(currentMonthDate, 1)#.strftime('%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    #------------------ Total Collection
    transactionCause="'','COLLECTION ERROR','ENTRY ERROR'"    #AND (sm_payment_collection.store_id='"+store_id+"') 
    condStr1=" (sm_payment_collection.cid = '"+c_id+"') AND (sm_payment_collection.depot_id='"+depot_id+"') AND (sm_payment_collection.payment_ym_date = '"+str(currentMonth)+"') AND (sm_payment_collection.status='Posted') AND (sm_payment_collection.transaction_cause IN ("+str(transactionCause)+"))"
    paymentRecords1="(SELECT sm_payment_collection.head_rowid as hRowId,ROUND(SUM(sm_payment_collection.collection_amount),2) as collAmt FROM sm_payment_collection WHERE ("+str(condStr1)+") GROUP BY sm_payment_collection.head_rowid ORDER BY sm_payment_collection.head_rowid)"
    
    records1="SELECT sm_invoice_head.depot_id as depot_id,SUM(sm_invoice_head.actual_total_tp) as actualTpAmt,SUM(sm_invoice_head.vat_total_amount) as vatTotalAmt,SUM(sm_invoice_head.discount) as discAmt,SUM(sm_invoice_head.sp_discount) as spDiscAmt,SUM(sm_invoice_head.adjust_amount) as adjustAmt,SUM(sm_invoice_head.return_tp) as retTpAmt,SUM(sm_invoice_head.return_vat) as retVatAmt,SUM(sm_invoice_head.return_discount) as retDiscAmt,SUM(sm_invoice_head.return_sp_discount) as retSpDiscAmt,SUM(smPay.collAmt) as collAmt FROM sm_invoice_head,"+str(paymentRecords1)+" as smPay WHERE ((sm_invoice_head.cid = '"+c_id+"') AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.id=smPay.hRowId) ) GROUP BY sm_invoice_head.depot_id"
    recordList1=db.executesql(records1,as_dict = True)
    
    collectionTp=0
    collectionVat=0
    collectionDisc=0
    collectionSpDisc=0
    for i in range(len(recordList1)):
        actualTpAmt=float(recordList1[i]['actualTpAmt'])
        vatTotalAmt=float(recordList1[i]['vatTotalAmt'])
        discAmt=float(recordList1[i]['discAmt'])
        spDiscAmt=float(recordList1[i]['spDiscAmt'])
        
        retTpAmt=float(recordList1[i]['retTpAmt'])
        retVatAmt=float(recordList1[i]['retVatAmt'])
        retDiscAmt=float(recordList1[i]['retDiscAmt'])
        retSpDiscAmt=float(recordList1[i]['retSpDiscAmt'])
        
        invTp=round(actualTpAmt,2)#-(retTpAmt+retSpDiscAmt) 
        invVat=round(vatTotalAmt,2)#-retVatAmt
        invDiscount=round(discAmt,2)#-retDiscAmt
        invSpDisc=round(spDiscAmt,2)#-retSpDiscAmt
        
        invNetAmt=round(invTp+invVat-(invDiscount+invSpDisc),2)
        
        collection=round(recordList1[i]['collAmt'],2)#invNetAmt-
        try:
            collTp=(invTp*collection)/invNetAmt
            collVat=(invVat*collection)/invNetAmt
            collDisc=(invDiscount*collection)/invNetAmt
            collSp=(invSpDisc*collection)/invNetAmt
            
            collectionTp=round(collTp,2)
            collectionVat=round(collVat,2)
            collectionDisc=round(collDisc,2)
            collectionSpDisc=round(collSp,2)
        except:
            pass
        break
    
    #------------------ opening Outstanding #AND (sm_invoice_head.store_id='"+store_id+"')
    condStr2="(sm_invoice_head.cid = '"+c_id+"') AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.invoice_ym_date < '"+str(currentMonth)+"') AND (sm_invoice_head.status='Invoiced')"
    condStr2+=" AND (round(sm_invoice_head.total_amount-(sm_invoice_head.return_tp+sm_invoice_head.return_vat-sm_invoice_head.return_discount)-sm_invoice_head.collection_amount,2)!=0)"
    records2="SELECT sm_invoice_head.depot_id as depot_id,SUM(sm_invoice_head.actual_total_tp) as actualTpAmt,SUM(sm_invoice_head.vat_total_amount) as vatTotalAmt,SUM(sm_invoice_head.discount) as discAmt,SUM(sm_invoice_head.sp_discount) as spDiscAmt,SUM(sm_invoice_head.adjust_amount) as adjustAmt,SUM(sm_invoice_head.return_tp) as retTpAmt,SUM(sm_invoice_head.return_vat) as retVatAmt,SUM(sm_invoice_head.return_discount) as retDiscAmt,SUM(sm_invoice_head.return_sp_discount) as retSpDiscAmt,SUM(sm_invoice_head.collection_amount) as collAmt FROM sm_invoice_head WHERE ("+str(condStr2)+") GROUP BY sm_invoice_head.depot_id"
    recordList2=db.executesql(records2,as_dict = True)
    
    openingTpOst=0
    openingVatOst=0
    openingDiscOst=0
    openingSpDiscOst=0
    for j in range(len(recordList2)):
        actualTpAmt=float(recordList2[j]['actualTpAmt'])
        vatTotalAmt=float(recordList2[j]['vatTotalAmt'])
        discAmt=float(recordList2[j]['discAmt'])
        spDiscAmt=float(recordList2[j]['spDiscAmt'])
        
        retTpAmt=float(recordList2[j]['retTpAmt'])
        retVatAmt=float(recordList2[j]['retVatAmt'])
        retDiscAmt=float(recordList2[j]['retDiscAmt'])
        retSpDiscAmt=float(recordList2[j]['retSpDiscAmt'])
        
        invTp=round(actualTpAmt-(retTpAmt+retSpDiscAmt),2)
        invVat=round(vatTotalAmt-retVatAmt,2)
        invDiscount=round(discAmt-retDiscAmt,2)
        invSpDisc=round(spDiscAmt-retSpDiscAmt,2)
        
        invNetAmt=round(invTp+invVat-(invDiscount+invSpDisc),2)
        
        outstanding=round(invNetAmt-recordList2[j]['collAmt'],2)
        try:
            outTp=(invTp*outstanding)/invNetAmt
            outVat=(invVat*outstanding)/invNetAmt
            outDisc=(invDiscount*outstanding)/invNetAmt
            outSp=(invSpDisc*outstanding)/invNetAmt
            
            openingTpOst=round(outTp,2)
            openingVatOst=round(outVat,2)
            openingDiscOst=round(outDisc,2)
            openingSpDiscOst=round(outSp,2)
        except:
            pass
        break
    
    #---------------------- Return this month but invoice previous #AND (sm_return_head.store_id='"+store_id+"') 
    condStr5=" (sm_return_head.cid = '"+c_id+"') AND (sm_return_head.depot_id='"+depot_id+"') AND (sm_return_head.ym_date = '"+str(currentMonth)+"') AND (sm_return_head.invoice_ym_date < '"+str(currentMonth)+"')  AND (sm_return_head.status='Returned')"
    records5="SELECT sm_return_head.depot_id as depot_id,SUM((sm_return_head.total_amount-sm_return_head.vat_total_amount+sm_return_head.discount)+sm_return_head.sp_discount) as retTpAmt,SUM(sm_return_head.vat_total_amount) as retVatAmt,SUM(sm_return_head.discount) as retDiscAmt,SUM(sm_return_head.sp_discount) as retSpDiscAmt FROM sm_return_head WHERE ( "+str(condStr5)+") GROUP BY sm_return_head.depot_id"
    recordList5=db.executesql(records5,as_dict = True)
    
    prevRetTp=0
    prevRetVat=0
    prevRetDisc=0
    prevRetSpDisc=0
    for n in range(len(recordList5)):        
        retTpAmt=float(recordList5[n]['retTpAmt'])
        retVatAmt=float(recordList5[n]['retVatAmt'])
        retDiscAmt=float(recordList5[n]['retDiscAmt'])
        retSpDiscAmt=float(recordList5[n]['retSpDiscAmt'])
        prevRetTp=round(retTpAmt,2)
        prevRetVat=round(retVatAmt,2)
        prevRetDisc=round(retDiscAmt,2)       
        prevRetSpDisc=round(retSpDiscAmt,2)   
        break
        
    #------------------------- net Sale    #AND (sm_invoice_head.store_id='"+store_id+"')
    condStr6="(sm_invoice_head.cid = '"+c_id+"') AND (sm_invoice_head.depot_id='"+depot_id+"') AND (sm_invoice_head.invoice_ym_date = '"+str(currentMonth)+"') AND (sm_invoice_head.status='Invoiced')"
    
    records6="SELECT sm_invoice_head.depot_id as depot_id,SUM(sm_invoice_head.actual_total_tp) as actualTpAmt,SUM(sm_invoice_head.vat_total_amount) as vatTotalAmt,SUM(sm_invoice_head.discount) as discAmt,SUM(sm_invoice_head.sp_discount) as spDiscAmt,SUM(sm_invoice_head.adjust_amount) as adjustAmt,SUM(sm_invoice_head.return_tp) as retTpAmt,SUM(sm_invoice_head.return_vat) as retVatAmt,SUM(sm_invoice_head.return_discount) as retDiscAmt,SUM(sm_invoice_head.return_sp_discount) as retSpDiscAmt FROM sm_invoice_head WHERE ("+str(condStr6)+") GROUP BY sm_invoice_head.depot_id"
    recordList6=db.executesql(records6,as_dict = True)
    
    salesTp=0
    salesVat=0
    salesDisc=0
    salesSpDisc=0
    for p in range(len(recordList6)):
        actualTpAmt=float(recordList6[p]['actualTpAmt'])
        vatTotalAmt=float(recordList6[p]['vatTotalAmt'])
        discAmt=float(recordList6[p]['discAmt'])
        spDiscAmt=float(recordList6[p]['spDiscAmt'])
        
        retTpAmt=float(recordList6[p]['retTpAmt'])
        retVatAmt=float(recordList6[p]['retVatAmt'])
        retDiscAmt=float(recordList6[p]['retDiscAmt'])
        retSpDiscAmt=float(recordList6[p]['retSpDiscAmt'])
        
        invTp=round(actualTpAmt-(retTpAmt+retSpDiscAmt),2)
        invVat=round(vatTotalAmt-retVatAmt,2)
        invDiscount=round(discAmt-retDiscAmt,2)
        invSpDisc=round(spDiscAmt-retSpDiscAmt,2)
        
        salesTp=invTp
        salesVat=invVat
        salesDisc=invDiscount
        salesSpDisc=invSpDisc
        break
    
    
    return dict(collectionTp=collectionTp,collectionVat=collectionVat,collectionDisc=collectionDisc,collectionSpDisc=collectionSpDisc,openingTpOst=openingTpOst,openingVatOst=openingVatOst,openingDiscOst=openingDiscOst,openingSpDiscOst=openingSpDiscOst,prevRetTp=prevRetTp,prevRetVat=prevRetVat,prevRetDisc=prevRetDisc,prevRetSpDisc=prevRetSpDisc,salesTp=salesTp,salesVat=salesVat,salesDisc=salesDisc,salesSpDisc=salesSpDisc,date_from=startDt,date_to=endDt,currentMonthDate=currentMonthDate,depot_id=depot_id,depotName=depot_name,store_id=store_id,storeName=store_name,page=page,items_per_page=items_per_page)    
    
#=============End Billal
