
def home():
    task_id='rm_analysis_view'
    access_permission=check_role(task_id)
    if (access_permission==False ):
        session.flash='Access is Denied'
        redirect (URL('default','home'))
        
    response.title='Report:Others'
    
    c_id=session.cid
    
    search_form =SQLFORM(db.sm_search_date)
    
    #-------------Billal
    btn_chk_dp_wise_inv=request.vars.btn_chk_dp_wise_inv
    btn_chk_dp_wise_inv_D=request.vars.btn_chk_dp_wise_inv_D
    
    btn_chk_dp_wise_inv_2=request.vars.btn_chk_dp_wise_inv_2
    btn_chk_dp_wise_inv_2_D=request.vars.btn_chk_dp_wise_inv_2_D
        
    btn_chk_dp_wise_doc=request.vars.btn_chk_dp_wise_doc
    btn_chk_dp_wise_doc_D=request.vars.btn_chk_dp_wise_doc_D
        
    btn_user_wise_inv=request.vars.btn_user_wise_inv
    btn_user_wise_inv_D=request.vars.btn_user_wise_inv_D
    
    btn_customer_info=request.vars.btn_customer_info
    btn_customer_info_D=request.vars.btn_customer_info_D
    
    btn_new_customer_info=request.vars.btn_new_customer_info
    btn_new_customer_info_D=request.vars.btn_new_customer_info_D
    
    btn_price_wise_product_sale=request.vars.btn_price_wise_product_sale
    btn_price_wise_product_sale_D=request.vars.btn_price_wise_product_sale_D
    
    btn_customer_type_wise_sales=request.vars.btn_customer_type_wise_sales
    btn_customer_type_wise_sales_D=request.vars.btn_customer_type_wise_sales_D
    
    btn_chk_incomp_inv=request.vars.btn_chk_incomp_inv
    btn_chk_incomp_inv_D=request.vars.btn_chk_incomp_inv_D
    
    
    #End Billal
    
    #--------------- Billal
    #     Billal
    if (btn_new_customer_info or btn_new_customer_info_D or btn_customer_type_wise_sales or btn_customer_type_wise_sales_D or btn_price_wise_product_sale or btn_price_wise_product_sale_D or btn_chk_incomp_inv or btn_chk_incomp_inv_D or btn_user_wise_inv or btn_user_wise_inv_D or btn_chk_dp_wise_doc or btn_chk_dp_wise_doc_D or btn_chk_dp_wise_inv_2 or btn_chk_dp_wise_inv_2_D or btn_chk_dp_wise_inv or btn_chk_dp_wise_inv_D):
        date_from=request.vars.from_dt_2
        date_to=request.vars.to_dt_2
        
        depot=str(request.vars.depot_id_others)
        store=str(request.vars.store_id_others) 
    
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
            if dateDiff>31:
                response.flash="Maximum 31 days allowed between Date Range"
            else:
                if ((depot=='') | (store=='')):
                    session.flash="Required Branch and Store"
                    redirect(URL(c='report_others',f='home'))
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
                        
                                            
                    # report function
                    if btn_chk_dp_wise_inv:                        
                        redirect (URL('dp_wise_invoice',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,store_id=store_id)))                    
                    elif btn_chk_dp_wise_inv_D:
                        redirect (URL('dp_wise_invoice_D',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,store_id=store_id)))                    
                    
                    elif btn_chk_dp_wise_inv_2:                        
                        redirect (URL('dp_wise_invoice_2',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,store_id=store_id)))                    
                    elif btn_chk_dp_wise_inv_2_D:
                        redirect (URL('dp_wise_invoice_2_D',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,store_id=store_id)))                    
                    
                    elif btn_chk_dp_wise_doc:                        
                        redirect (URL('dp_wise_doc_list',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,store_id=store_id)))                    
                    elif btn_chk_dp_wise_doc_D:
                        redirect (URL('dp_wise_doc_list_D',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,store_id=store_id)))                    
                                            
                    elif btn_new_customer_info:                        
                        redirect (URL('customer_info_new',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,store_id=store_id)))                    
                    elif btn_new_customer_info_D:
                        redirect (URL('customer_info_new_D',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,store_id=store_id)))                    
                    
                    elif btn_user_wise_inv:
                        userID=request.vars.depot_user
                        if userID=='' or userID==None:
                            response.flash='Required User ID'
                        else:                        
                            redirect (URL('user_wise_invoice',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,store_id=store_id,user_id=userID)))                    
                    elif btn_user_wise_inv_D:
                        userID=request.vars.depot_user
                        if userID=='' or userID==None:
                            response.flash='Required User ID'
                        else:                        
                            redirect (URL('user_wise_invoice_D',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,store_id=store_id,user_id=userID)))                    
                    
                    elif btn_price_wise_product_sale:                        
                        redirect (URL('pricelist_wise_product_sales',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,store_id=store_id)))                    
                    elif btn_price_wise_product_sale_D:
                        redirect (URL('pricelist_wise_product_sales_D',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,store_id=store_id)))                    
                    
                    elif btn_customer_type_wise_sales:                        
                        redirect (URL('customer_type_wise_sales_details',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,store_id=store_id)))                    
                    elif btn_customer_type_wise_sales_D:
                        response.flash='btn_price_wise_product_sale_D'
                                
                    elif btn_chk_incomp_inv:                        
                        redirect (URL('incomplete_invoice',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,store_id=store_id)))                    
                    elif btn_chk_incomp_inv_D:
                        redirect (URL('incomplete_invoice_D',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,store_id=store_id)))                    
    
                        #----------End Billal
    
    elif btn_customer_info or btn_customer_info_D:
        depot=str(request.vars.depot_id_others)
        store=str(request.vars.store_id_others) 
        
        if ((depot=='') | (store=='')):
            session.flash="Required Branch and Store"
            redirect(URL(c='report_others',f='home'))
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
            
            if btn_customer_info:                        
                redirect (URL('customer_info',vars=dict(depot_id=depot_id,store_id=store_id)))                    
            elif btn_customer_info_D:
                redirect (URL('customer_info_D',vars=dict(depot_id=depot_id,store_id=store_id)))
            
        
        
    return dict(search_form=search_form)
    

#===================================================others Billal



def incomplete_invoice():
    c_id=session.cid
    
    response.title='14 Checking Incomplete Invoice'
    
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
    qset=qset((db.sm_invoice_head.delivery_date>=startDt)&(db.sm_invoice_head.delivery_date<=endDt))
    qset=qset(db.sm_invoice_head.status=='Submitted')
    records=qset.select(db.sm_invoice_head.delivery_date,db.sm_invoice_head.order_datetime,db.sm_invoice_head.depot_id,db.sm_invoice_head.sl,db.sm_invoice_head.market_id,db.sm_invoice_head.market_name,orderby=db.sm_invoice_head.id)
   
    return dict(records=records,date_from=startDt,date_to=endDt,page=page,items_per_page=items_per_page)    


def incomplete_invoice_D():
    c_id=session.cid
    
    response.title='14 Checking Incomplete Invoice'
    
    fromDate=request.vars.date_from
    toDate=request.vars.date_to
    
    depot_id=str(request.vars.depot_id).strip()
    store_id=str(request.vars.store_id).strip()   
    
    depot_name=''
    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
    if depotRow:
        depot_name=depotRow[0].name
    
    store_name=''
    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name)
    if storeRow:
        store_name=storeRow[0].store_name
    
    
    try:        
        startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        startDt=''                
        
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    
    myString='14 Checking Incomplete Invoice\n\n'
    
    myString+='Date From:,'+str(datetime.datetime.strptime(str(startDt),'%Y-%m-%d').strftime('%d-%b-%Y'))+'\n'
    myString+='Date To:,'+str(datetime.datetime.strptime(str(endDt),'%Y-%m-%d').strftime('%d-%b-%Y'))+'\n'
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depot_name)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(store_name)+'\n\n'
    


    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.depot_id==depot_id)
    qset=qset(db.sm_invoice_head.store_id==store_id)
    qset=qset((db.sm_invoice_head.delivery_date>=startDt)&(db.sm_invoice_head.delivery_date<=endDt))
    qset=qset(db.sm_invoice_head.status=='Submitted')
    records=qset.select(db.sm_invoice_head.delivery_date,db.sm_invoice_head.order_datetime,db.sm_invoice_head.depot_id,db.sm_invoice_head.sl,db.sm_invoice_head.market_id,db.sm_invoice_head.market_name,orderby=db.sm_invoice_head.delivery_date)
    
    
    myString+='SHIDATE,INVNO,ORDER DATE,ORDER TIME,MARKET ID,MARKET NAME'+'\n'
    
    for row in records:
        delivery_date=str(row.delivery_date.strftime('%d-%b-%y'))
        invNo=session.prefix_invoice+'INV'+str(row.depot_id)+'-'+str(row.sl)
        order_datetime=str(row.order_datetime.strftime('%d-%b-%y'))
        orderTime=str(row.order_datetime)[10:]
        market_id=str(row.market_id)
        market_name=str(row.market_name)
        
        
        myString+=str(delivery_date)+','+str(invNo)+','+str(order_datetime)+','+str(orderTime)+','+str(market_id)+','+str(market_name)+'\n'
            
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=pricelist_wise_product_sales_d.csv'   
    return str(myString)
        
    
    return dict(records=records,date_from=startDt,date_to=endDt,page=page,items_per_page=items_per_page)    





#def customer_type_wise_sales_details():
#    
#    c_id=session.cid
#    
#    response.title='20 Customer Type Wise Sales Details'
#    
#    fromDate=request.vars.date_from
#    toDate=request.vars.date_to
#    
#    depot_id=str(request.vars.depot_id).strip()
#    store_id=str(request.vars.store_id).strip()   
#    
#    depot_name=''
#    depotRow=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
#    if depotRow:
#        depot_name=depotRow[0].name
#    
#    store_name=''
#    storeRow=db((db.sm_depot_store.cid==c_id)&(db.sm_depot_store.depot_id==depot_id)&(db.sm_depot_store.store_id==store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
#    if storeRow:
#        store_name=storeRow[0].store_name
#    
#    
#    try:        
#        startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')
#    except:
#        startDt=''                
#        
#    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
#    
#    #--------------paging
#    if len(request.args):
#        page=int(request.args[0])
#    else:
#        page=0
#    items_per_page=20   
#    limitby=(page*items_per_page,(page+1)*items_per_page+1)
#    #---------------end paging
#    
#    
##    invRows="SELECT invoice_date,depot_id,sl as invSl,client_id,client_name,cl_category_name,total_amount as invTotal,vat_total_amount as invVat,discount as invDisc FROM sm_invoice_head where cid = '"+c_id+"' and depot_id = '"+depot_id+"' and store_id = '"+store_id+"' and invoice_date >= '"+str(startDt)+"' and invoice_date <= '"+str(endDt)+"' ORDER BY sl"
##    invDictData=db.executesql(invRows,as_dict = True)
#    
#    
#    retRows="SELECT invoice_sl as invSl,sum(total_amount) as rAmt,sum(vat_total_amount) as rVat,sum(discount) as rDisc FROM sm_return_head where cid = '"+c_id+"' and depot_id = '"+depot_id+"' and store_id = '"+store_id+"' and return_date >= '"+str(startDt)+"' and return_date <= '"+str(endDt)+"' group by invoice_sl"
#    retDictData=db.executesql(retRows,as_dict = True)
#    
#     
#    
#    qset=db()
#    qset=qset(db.sm_invoice_head.cid==c_id)
#    qset=qset(db.sm_invoice_head.depot_id==depot_id)
#    qset=qset(db.sm_invoice_head.store_id==store_id)
#    qset=qset((db.sm_invoice_head.invoice_date>=startDt)&(db.sm_invoice_head.invoice_date<=endDt))
#    
#    invRecrd=qset.select(db.sm_invoice_head.sl,db.sm_invoice_head.invoice_date,db.sm_invoice_head.depot_id,db.sm_invoice_head.client_id,db.sm_invoice_head.client_name,db.sm_invoice_head.cl_category_name,db.sm_invoice_head.total_amount,db.sm_invoice_head.vat_total_amount,db.sm_invoice_head.discount)
#    invDataList=[]
#    for inv in invRecrd:
#        sl=inv.sl
#        invoice_date=inv.invoice_date
#        depot_id=inv.depot_id
#        client_id=inv.client_id
#        client_name=inv.client_name
#        cl_category_name=inv.cl_category_name
#        total_amount=inv.total_amount
#        vat_total_amount=inv.vat_total_amount
#        discount=inv.discount
#        
#        dictInvData={'invSl':sl,'invoice_date':invoice_date,'depot_id':depot_id,'client_id':client_id,'client_name':client_name,'cl_category_name':cl_category_name,'total_amount':total_amount,'vat_total_amount':vat_total_amount,'discount':discount,'r_total_amount':'0','r_vat_total_amount':'0','r_discount':'0'}
#        invDataList.append(dictInvData)
# 
#    
#    for i in range(len(invDataList)):
#        invSlStr=invDataList[i]
#        inv_sl=invSlStr['invSl']
#        
#        
#        rec_index=-1
#        try:
#            rec_index=str(map(itemgetter('invSl'), retDictData).index(inv_sl))    
#        except:
#            rec_index=-1
#        
#        
#        if (rec_index!=-1):
#            retDictData=retDictData[int(rec_index)]             
#            
#            invSlStr['r_total_amount']=str(retDictData['rAmt'])
#            invSlStr['r_vat_total_amount']=str(retDictData['rVat'])
#            invSlStr['r_discount']=str(retDictData['rDisc'])
          
##    dateRecords="SELECT a.invoice_date,a.depot_id,a.sl, a.client_id, a.client_name, a.cl_category_name,a.total_amount as invTotal, a.vat_total_amount as invVat,a.discount as invDisc,b.return_date,sum(b.total_amount) as rtTotalAmt,b.vat_total_amount as rtVat,b.discount as rtDisc FROM sm_invoice_head a LEFT JOIN sm_return_head b ON a.sl=b.invoice_sl where a.cid = '"+c_id+"' and a.depot_id = '"+depot_id+"' and a.store_id = '"+store_id+"' and a.invoice_date >= '"+str(startDt)+"' and a.invoice_date <= '"+str(endDt)+"' GROUP BY a.sl ORDER BY a.sl"
##    
##    records=db.executesql(dateRecords,as_dict = True) 
#    
#    return dict(invDataList=invDataList,date_from=startDt,date_to=endDt,depotName=depot_name,storeName=store_name,page=page,items_per_page=items_per_page) 

def pricelist_wise_product_sales():
    c_id=session.cid
    
    response.title='26 Pricelist Wise Product Sales Statement'
    
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
    qset=qset(db.sm_invoice.depot_id==depot_id)
    qset=qset(db.sm_invoice.store_id==store_id)
    qset=qset((db.sm_invoice.invoice_date>=startDt)&(db.sm_invoice.invoice_date<=endDt))
    qset=qset(db.sm_invoice.status=='Invoiced')
    
    #------------------------premium
    premiumList=[]
    premQset=qset(db.sm_invoice.short_note.like('%Premium TP%'))    
    premRecords=premQset.select(db.sm_invoice.item_id,db.sm_invoice.item_name,db.sm_invoice.item_unit,db.sm_invoice.quantity.sum(),db.sm_invoice.return_qty.sum(),groupby=db.sm_invoice.item_id,orderby=db.sm_invoice.item_name)
    for premRow in premRecords:
        item_id=premRow.sm_invoice.item_id
        item_name=premRow.sm_invoice.item_name
        item_unit=premRow.sm_invoice.item_unit        
        quantity=int(premRow[db.sm_invoice.quantity.sum()])
        return_qty=int(premRow[db.sm_invoice.return_qty.sum()])        
        premiumList.append({'item_id':item_id,'item_name':item_name,'item_unit':item_unit,'bonusQty':0,'regQty':0,'premQty':quantity,'retBonusQty':0,'retRegQty':0,'retPremQty':return_qty})
        
    #-------------------- bonus
    bonusList=[]
    bonusQset=qset(db.sm_invoice.bonus_qty>0)    
    bonusRecords=bonusQset.select(db.sm_invoice.item_id,db.sm_invoice.item_name,db.sm_invoice.item_unit,db.sm_invoice.bonus_qty.sum(),db.sm_invoice.return_bonus_qty.sum(),groupby=db.sm_invoice.item_id,orderby=db.sm_invoice.item_name)
    for bonusRow in bonusRecords:
        item_id=bonusRow.sm_invoice.item_id
        item_name=bonusRow.sm_invoice.item_name
        item_unit=bonusRow.sm_invoice.item_unit        
        bonus_qty=int(bonusRow[db.sm_invoice.bonus_qty.sum()])
        return_bonus_qty=int(bonusRow[db.sm_invoice.return_bonus_qty.sum()])                
        bonusList.append({'item_id':item_id,'item_name':item_name,'item_unit':item_unit,'bonusQty':bonus_qty,'regQty':0,'premQty':0,'retBonusQty':return_bonus_qty,'retRegQty':0,'retPremQty':0})
        
    #-------------------regular
    regQset=qset(db.sm_invoice.bonus_qty==0)    
    regRecords=regQset.select(db.sm_invoice.item_id,db.sm_invoice.item_name,db.sm_invoice.item_unit,db.sm_invoice.quantity.sum(),db.sm_invoice.return_qty.sum(),groupby=db.sm_invoice.item_id,orderby=db.sm_invoice.item_name)
    regularList=[]
    for regRow in regRecords:
        item_id=regRow.sm_invoice.item_id
        item_name=regRow.sm_invoice.item_name
        item_unit=regRow.sm_invoice.item_unit
        
        quantity=int(regRow[db.sm_invoice.quantity.sum()])
        return_qty=int(regRow[db.sm_invoice.return_qty.sum()])
        
        premQty=0
        retPremQty=0        
        #----------------
        sec_index=-1
        try:
            sec_index=str(map(itemgetter('item_id'), premiumList).index(item_id))    
        except:
            sec_index=-1
            
        if (sec_index!=-1):
            secDictData=premiumList[int(sec_index)]
            
            premQty=int(secDictData['premQty'])
            retPremQty=int(secDictData['retPremQty'])
            
            del premiumList[int(sec_index)]
        #---------------        
        regQty=quantity-premQty
        retRegQty=return_qty-retPremQty
        
        regularList.append({'item_id':item_id,'item_name':item_name,'item_unit':item_unit,'bonusQty':0,'regQty':regQty,'premQty':premQty,'retBonusQty':0,'retRegQty':retRegQty,'retPremQty':retPremQty})
    
    
    # premium,regular and bonus
    itemList=[]
    itemList=regularList+premiumList
    
    for i in range(len(itemList)):
        itemDict=itemList[i]
        item_id=itemDict['item_id']
        
        bonusQty=0
        retBonusQty=0
        #----------------
        sec_index=-1
        try:
            sec_index=str(map(itemgetter('item_id'), bonusList).index(item_id))    
        except:
            sec_index=-1
            
        if (sec_index!=-1):
            secDictData=bonusList[int(sec_index)]
            
            itemDict['bonusQty']=int(secDictData['bonusQty'])
            itemDict['retBonusQty']=int(secDictData['retBonusQty'])
            
            del bonusList[int(sec_index)]
        #---------------  
    
    recordList=[]
    recordList=itemList+bonusList    
    recordList.sort(key=itemgetter('item_name'), reverse=False) 
    
    return dict(recordList=recordList,date_from=startDt,date_to=endDt,depotName=depot_name,storeName=store_name,page=page,items_per_page=items_per_page)    


def pricelist_wise_product_sales_D():
    c_id=session.cid
    
    response.title='26 Pricelist Wise Product Sales Statement'
    
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
    
    
    
    qset=db()
    qset=qset(db.sm_invoice.cid==c_id)
    qset=qset(db.sm_invoice.depot_id==depot_id)
    qset=qset(db.sm_invoice.store_id==store_id)
    qset=qset((db.sm_invoice.invoice_date>=startDt)&(db.sm_invoice.invoice_date<=endDt))
    qset=qset(db.sm_invoice.status=='Invoiced')
    
    #------------------------premium
    premiumList=[]
    premQset=qset(db.sm_invoice.short_note.like('%Premium TP%'))    
    premRecords=premQset.select(db.sm_invoice.item_id,db.sm_invoice.item_name,db.sm_invoice.item_unit,db.sm_invoice.quantity.sum(),db.sm_invoice.return_qty.sum(),groupby=db.sm_invoice.item_id,orderby=db.sm_invoice.item_name)
    for premRow in premRecords:
        item_id=premRow.sm_invoice.item_id
        item_name=premRow.sm_invoice.item_name
        item_unit=premRow.sm_invoice.item_unit        
        quantity=int(premRow[db.sm_invoice.quantity.sum()])
        return_qty=int(premRow[db.sm_invoice.return_qty.sum()])        
        premiumList.append({'item_id':item_id,'item_name':item_name,'item_unit':item_unit,'bonusQty':0,'regQty':0,'premQty':quantity,'retBonusQty':0,'retRegQty':0,'retPremQty':return_qty})
        
    #-------------------- bonus
    bonusList=[]
    bonusQset=qset(db.sm_invoice.bonus_qty>0)    
    bonusRecords=bonusQset.select(db.sm_invoice.item_id,db.sm_invoice.item_name,db.sm_invoice.item_unit,db.sm_invoice.bonus_qty.sum(),db.sm_invoice.return_bonus_qty.sum(),groupby=db.sm_invoice.item_id,orderby=db.sm_invoice.item_name)
    for bonusRow in bonusRecords:
        item_id=bonusRow.sm_invoice.item_id
        item_name=bonusRow.sm_invoice.item_name
        item_unit=bonusRow.sm_invoice.item_unit        
        bonus_qty=int(bonusRow[db.sm_invoice.bonus_qty.sum()])
        return_bonus_qty=int(bonusRow[db.sm_invoice.return_bonus_qty.sum()])                
        bonusList.append({'item_id':item_id,'item_name':item_name,'item_unit':item_unit,'bonusQty':bonus_qty,'regQty':0,'premQty':0,'retBonusQty':return_bonus_qty,'retRegQty':0,'retPremQty':0})
        
    #-------------------regular
    regQset=qset(db.sm_invoice.bonus_qty==0)    
    regRecords=regQset.select(db.sm_invoice.item_id,db.sm_invoice.item_name,db.sm_invoice.item_unit,db.sm_invoice.quantity.sum(),db.sm_invoice.return_qty.sum(),groupby=db.sm_invoice.item_id,orderby=db.sm_invoice.item_name)
    regularList=[]
    for regRow in regRecords:
        item_id=regRow.sm_invoice.item_id
        item_name=regRow.sm_invoice.item_name
        item_unit=regRow.sm_invoice.item_unit
        
        quantity=int(regRow[db.sm_invoice.quantity.sum()])
        return_qty=int(regRow[db.sm_invoice.return_qty.sum()])
        
        premQty=0
        retPremQty=0        
        #----------------
        sec_index=-1
        try:
            sec_index=str(map(itemgetter('item_id'), premiumList).index(item_id))    
        except:
            sec_index=-1
            
        if (sec_index!=-1):
            secDictData=premiumList[int(sec_index)]
            
            premQty=int(secDictData['premQty'])
            retPremQty=int(secDictData['retPremQty'])
            
            del premiumList[int(sec_index)]
        #---------------        
        regQty=quantity-premQty
        retRegQty=return_qty-retPremQty
        
        regularList.append({'item_id':item_id,'item_name':item_name,'item_unit':item_unit,'bonusQty':0,'regQty':regQty,'premQty':premQty,'retBonusQty':0,'retRegQty':retRegQty,'retPremQty':retPremQty})
    
    
    # premium,regular and bonus
    itemList=[]
    itemList=regularList+premiumList
    
    for i in range(len(itemList)):
        itemDict=itemList[i]
        item_id=itemDict['item_id']
        
        bonusQty=0
        retBonusQty=0
        #----------------
        sec_index=-1
        try:
            sec_index=str(map(itemgetter('item_id'), bonusList).index(item_id))    
        except:
            sec_index=-1
            
        if (sec_index!=-1):
            secDictData=bonusList[int(sec_index)]
            
            itemDict['bonusQty']=int(secDictData['bonusQty'])
            itemDict['retBonusQty']=int(secDictData['retBonusQty'])
            
            del bonusList[int(sec_index)]
        #---------------  
    
    recordList=[]
    recordList=itemList+bonusList    
    recordList.sort(key=itemgetter('item_name'), reverse=False) 
    
    #==================
    myString='26 Pricelist Wise Product Sales Statement\n\n'
    
    myString+='Date From:,'+str(datetime.datetime.strptime(str(startDt),'%Y-%m-%d').strftime('%d-%b-%Y'))+'\n'
    myString+='Date To:,'+str(datetime.datetime.strptime(str(endDt),'%Y-%m-%d').strftime('%d-%b-%Y'))+'\n'
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depot_name)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(store_name)+'\n\n'
    
    
    myString+='Product ID,Product Name,UOM,Invoice-Bonus,Invoice-Regular,Invoice-Premium,Return-Bonus,Return-Regular,Return-Premium,Net-Bonus,Net-Regular,Net-Premium'+'\n'
    
    totalBonusQty=0
    totalRtBonusQty=0    
    totalRegQty=0    
    totalRegRtQty=0
    totalPremQty=0    
    totalPremRtQty=0    
    totalNetBonusQty=0
    totalNetRegQty=0
    totalNetPremQty=0
    
    for i in range(len(recordList)): 
        dictData=recordList[i]
        
        item_id=dictData['item_id']
        item_name=dictData['item_name']
        item_unit=dictData['item_unit']
        
        bonusQty=dictData['bonusQty'] 
        retBonusQty=dictData['retBonusQty']  
        regQty=dictData['regQty']  
        retRegQty=dictData['retRegQty']  
        premQty=dictData['premQty']  
        retPremQty=dictData['retPremQty']      
        netBonusQty=bonusQty-retBonusQty
        netRegQty=regQty-retRegQty
        netPremQty=premQty-retPremQty
        
        totalBonusQty+=bonusQty 
        totalRtBonusQty+=retBonusQty  
        totalRegQty+=regQty  
        totalRegRtQty+=retRegQty  
        totalPremQty+=premQty  
        totalPremRtQty+=retPremQty
        totalNetBonusQty+=netBonusQty
        totalNetRegQty+=netRegQty
        totalNetPremQty+=netPremQty
        
        myString+=str(item_id)+','+str(item_name)+','+str(item_unit)+','+str(bonusQty)+','+str(regQty)+','+str(premQty)+','+str(retBonusQty)+','+str(retRegQty)+','+str(retPremQty)+','+str(netBonusQty)+','+str(netRegQty)+','+str(netPremQty)+'\n'
        
    myString+='Total,,,'+str(totalBonusQty)+','+str(totalRegQty)+','+str(totalPremQty)+','+str(totalRtBonusQty)+','+str(totalRegRtQty)+','+str(totalPremRtQty)+','+str(totalNetBonusQty)+','+str(totalNetRegQty)+','+str(totalNetPremQty)+'\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=pricelist_wise_product_sales_d.csv'   
    return str(myString)
        

       

def customer_info_new():
    c_id=session.cid
    
    response.title='New Customer Information'
    
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
    
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    nextDate=endDt+datetime.timedelta(days=1)
    
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
    qset=qset(db.sm_client.depot_id==depot_id)
    qset=qset(db.sm_client.store_id==store_id)
    qset=qset((db.sm_client.created_on>=startDt)&(db.sm_client.created_on<nextDate))
    records=qset.select(db.sm_client.ALL,orderby=~db.sm_client.name)
       
    return dict(records=records,date_from=startDt,date_to=endDt,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,page=page,items_per_page=items_per_page)    

def customer_info_new_D():
    c_id=session.cid
    
    response.title='New Customer Information'
    
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
    
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    nextDate=endDt+datetime.timedelta(days=1)
    
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
    qset=qset(db.sm_client.depot_id==depot_id)
    qset=qset(db.sm_client.store_id==store_id)
    qset=qset((db.sm_client.created_on>=startDt)&(db.sm_client.created_on<nextDate))
    records=qset.select(db.sm_client.ALL,orderby=~db.sm_client.name)
    
    
    myString='16.3 Customer Information\n'
    
    myString+='Date From:,'+str(datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%d-%b-%Y'))+'\n'
    myString+='Date To:,'+str(datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%d-%b-%Y'))+'\n'
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depot_name)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(store_name)+'\n\n'
    
       
    sl=0
    myString+='SL,New ID,Old ID,Name,Territory,Branch ID,Branch Name,Store ID,Store Name,Category ID,Category Name,Sub Category ID,\
    Sub Category Name,Branch Belt,Contact Name,Contact 1,Contact 2,Address,Market ID,Market Name,Thana ID,Thana,District,\
    Drug Registration Number,NID,Doctor,Status'+'\n'
    
    for row in records:
        sl+=1
        
        client_id=row.client_id
        client_old_id=row.client_old_id
        name=str(row.name).replace(',',' ')
        area_id=row.area_id
        depot_id=row.depot_id
        depot_name=str(row.depot_name).replace(',',' ')
        store_id=row.store_id
        store_name=str(row.store_name).replace(',',' ')
        category_id=row.category_id
        category_name=str(row.category_name).replace(',',' ')
        sub_category_id=row.sub_category_id
        sub_category_name=str(row.sub_category_name).replace(',',' ')
        depot_belt_name=row.depot_belt_name
        owner_name=str(row.owner_name).replace(',',' ')
        contact_no1=row.contact_no1
        contact_no2=row.contact_no2
        address=str(row.address).replace(',',' ')
        market_id=row.market_id
        market_name=str(row.market_name).replace(',',' ')
        thana_id=row.thana_id
        thana=str(row.thana).replace(',',' ') 
        district_id=row.district_id 
        drug_registration_num=row.drug_registration_num 
        nid=row.nid 
        doctor=row.doctor         
        status=row.status 
        
        if category_id=='000':
            category_id=''
            category_name=''
            
        if sub_category_id=='000':
            sub_category_id=''
            sub_category_name=''
            
        if owner_name=='Blank':
            owner_name=''
        
        if contact_no1==None:
            contact_no1=''
        
        if contact_no2==None:
            contact_no2=''
        
        if market_id=='0':
            market_id=''
            market_name=''
        
        if thana_id==None:
            thana_id=''
            thana=''  
        
        if district_id==None:
            district_id=''  
        
        if drug_registration_num=='0':
            drug_registration_num=''  
        
        if nid==None:
            nid=''
        if doctor==None:
            doctor=''          
        
            
        #------------------------        
        myString+=str(sl)+','+str(client_id)+','+str(client_old_id)+','+str(name)+','+str(area_id)+','+str(depot_id)+','+\
        str(depot_name)+','+str(store_id)+','+str(store_name)+','+str(category_id)+','+str(category_name)+','+str(sub_category_id)+','+\
        str(sub_category_name)+','+str(depot_belt_name)+','+str(owner_name)+','+str(contact_no1)+','+str(contact_no2)+','+\
        str(address)+','+str(market_id)+','+str(market_name)+','+str(thana_id)+','+str(thana)+','+str(district_id)+','+\
        str(drug_registration_num)+','+str(nid)+','+str(doctor)+','+str(status)+'\n'
    
        
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=customer_information_new.csv'   
    return str(myString)
       
    
    

def customer_info():
    c_id=session.cid
    
    response.title='Customer Information'
    
    
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
    qset=qset(db.sm_client.depot_id==depot_id)
    qset=qset(db.sm_client.store_id==store_id)
    records=qset.select(db.sm_client.ALL,orderby=~db.sm_client.name)
       
    return dict(records=records,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,page=page,items_per_page=items_per_page)    

def customer_info_D():
    c_id=session.cid
    
    response.title='Customer Information'
    
    
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
    qset=qset(db.sm_client.depot_id==depot_id)
    qset=qset(db.sm_client.store_id==store_id)
    records=qset.select(db.sm_client.ALL,orderby=~db.sm_client.name)
    
    
    myString='16.2 Customer Information\n'
    
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depot_name)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(store_name)+'\n\n'
    
       
    sl=0
    myString+='SL,New ID,Old ID,Name,Territory,Branch ID,Branch Name,Store ID,Store Name,Category ID,Category Name,Sub Category ID,\
    Sub Category Name,Branch Belt,Contact Name,Contact 1,Contact 2,Address,Market ID,Market Name,Thana ID,Thana,District,\
    Drug Registration Number,NID,Doctor,Status'+'\n'
    
    for row in records:
        sl+=1
        
        client_id=row.client_id
        client_old_id=row.client_old_id
        name=str(row.name).replace(',',' ')
        area_id=row.area_id
        depot_id=row.depot_id
        depot_name=str(row.depot_name).replace(',',' ')
        store_id=row.store_id
        store_name=str(row.store_name).replace(',',' ')
        category_id=row.category_id
        category_name=str(row.category_name).replace(',',' ')
        sub_category_id=row.sub_category_id
        sub_category_name=str(row.sub_category_name).replace(',',' ')
        depot_belt_name=row.depot_belt_name
        owner_name=str(row.owner_name).replace(',',' ')
        contact_no1=row.contact_no1
        contact_no2=row.contact_no2
        address=str(row.address).replace(',',' ')
        market_id=row.market_id
        market_name=str(row.market_name).replace(',',' ')
        thana_id=row.thana_id
        thana=str(row.thana).replace(',',' ') 
        district_id=row.district_id 
        drug_registration_num=row.drug_registration_num 
        nid=row.nid 
        doctor=row.doctor         
        status=row.status 
        
        if category_id=='000':
            category_id=''
            category_name=''
            
        if sub_category_id=='000':
            sub_category_id=''
            sub_category_name=''
            
        if owner_name=='Blank':
            owner_name=''
        
        if contact_no1==0:
            contact_no1=''
        
        if contact_no2==0:
            contact_no2=''
        
        if market_id=='0':
            market_id=''
            market_name=''
        
        if thana_id==None:
            thana_id=''
            thana=''  
        
        if district_id=='0':
            district_id=''  
        
        if drug_registration_num=='0':
            drug_registration_num=''  
        
        if nid==0:
            nid=''          
        
            
        #------------------------        
        myString+=str(sl)+','+str(client_id)+','+str(client_old_id)+','+str(name)+','+str(area_id)+','+str(depot_id)+','+\
        str(depot_name)+','+str(store_id)+','+str(store_name)+','+str(category_id)+','+str(category_name)+','+str(sub_category_id)+','+\
        str(sub_category_name)+','+str(depot_belt_name)+','+str(owner_name)+','+str(contact_no1)+','+str(contact_no2)+','+\
        str(address)+','+str(market_id)+','+str(market_name)+','+str(thana_id)+','+str(thana)+','+str(district_id)+','+\
        str(drug_registration_num)+','+str(nid)+','+str(doctor)+','+str(status)+'\n'
    
        
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=customer_information.csv'   
    return str(myString)

def user_wise_invoice():
    c_id=session.cid
    
    response.title='32 User Wise Invoice'
    
    fromDate=request.vars.date_from
    toDate=request.vars.date_to
    userID=request.vars.user_id
    
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
    qset=qset((db.sm_invoice_head.invoice_date>=startDt)&(db.sm_invoice_head.invoice_date<=endDt))
    qset=qset(db.sm_invoice_head.posted_by==userID)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    records=qset.select(db.sm_invoice_head.invoice_date,db.sm_invoice_head.client_id,db.sm_invoice_head.client_name,db.sm_invoice_head.shipment_no,db.sm_invoice_head.depot_id,db.sm_invoice_head.order_sl,db.sm_invoice_head.total_amount,orderby=db.sm_invoice_head.invoice_date)
    
    return dict(records=records,date_from=startDt,date_to=endDt,userID=userID,page=page,items_per_page=items_per_page)    


def user_wise_invoice_D():
    c_id=session.cid
    
    response.title='32 User Wise Invoice'
    
    fromDate=request.vars.date_from
    toDate=request.vars.date_to
    userID=request.vars.user_id
    
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
    
 
    myString='32 User Wise Invoice\n'
    
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depot_name)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(store_name)+'\n'  
    myString+='User ID'+','+str(userID)+'\n\n'  
    
    myString+='Date,Customer ID,Customer Name, Invoice Number, Shipment No, Invoice Total'+'\n'
    
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.depot_id==depot_id)
    qset=qset(db.sm_invoice_head.store_id==store_id)
    qset=qset((db.sm_invoice_head.invoice_date>=startDt)&(db.sm_invoice_head.invoice_date<=endDt))
    qset=qset(db.sm_invoice_head.posted_by==userID)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    records=qset.select(db.sm_invoice_head.invoice_date,db.sm_invoice_head.client_id,db.sm_invoice_head.client_name,db.sm_invoice_head.shipment_no,db.sm_invoice_head.depot_id,db.sm_invoice_head.order_sl,db.sm_invoice_head.total_amount,orderby=db.sm_invoice_head.invoice_date)
    
    for row in records:
        invoice_date=row.invoice_date.strftime('%d-%b-%y')
        client_id=row.client_id
        client_name=row.client_name
        shipment_no=row.shipment_no
        depot_id=row.depot_id
        order_sl=row.order_sl
        invoiceRef=session.prefix_invoice+'INV'+str(row.depot_id)+'-'+str(row.order_sl)
        total_amount=row.total_amount
        
        myString+=str(invoice_date)+','+str(client_id)+','+str(client_name)+','+str(shipment_no)+','+str(invoiceRef)+','+str(total_amount)+',\n'
        
    
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=user_wise_inv_d.csv'   
    return str(myString)    
    



def dp_wise_doc_list():
    c_id=session.cid
    
    response.title='29 DP Wise Document List'
    
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
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    

    invList=[]    
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.depot_id==depot_id)
    qset=qset(db.sm_invoice_head.store_id==store_id)
    qset=qset((db.sm_invoice_head.invoice_date>=startDt)&(db.sm_invoice_head.invoice_date<=endDt))
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    dMRecords=qset.select(db.sm_invoice_head.d_man_id,db.sm_invoice_head.d_man_name.max(),db.sm_invoice_head.id.count(),db.sm_invoice_head.actual_total_tp.sum(),groupby=db.sm_invoice_head.d_man_id)
    for dmRow in dMRecords:
        d_man_id=dmRow.sm_invoice_head.d_man_id
        d_man_name=dmRow[db.sm_invoice_head.d_man_name.max()]
        invCount=dmRow[db.sm_invoice_head.id.count()]
        invTpAmt=dmRow[db.sm_invoice_head.actual_total_tp.sum()]        
        invDPData={'d_man_id':d_man_id,'d_man_name':d_man_name,'invCount':invCount,'invTpAmt':invTpAmt,'retCount':0,'retTpAmt':0,'invData':'','retData':''}
        invList.append(invDPData)
        
    
    retList=[]
    qset2=db()
    qset2=qset2(db.sm_return_head.cid==c_id)
    qset2=qset2(db.sm_return_head.depot_id==depot_id)
    qset2=qset2(db.sm_return_head.store_id==store_id)
    qset2=qset2((db.sm_return_head.return_date>=startDt)&(db.sm_return_head.return_date<=endDt))
    qset2=qset2(db.sm_return_head.status=='Returned')
    dMRecords2=qset2.select(db.sm_return_head.d_man_id,db.sm_return_head.d_man_name.max(),db.sm_return_head.id.count(),db.sm_return_head.total_amount.sum(),db.sm_return_head.vat_total_amount.sum(),db.sm_return_head.discount.sum(),db.sm_return_head.sp_discount.sum(),groupby=db.sm_return_head.d_man_id)
    
    for dmRow2 in dMRecords2:
        d_man_id=dmRow2.sm_return_head.d_man_id
        d_man_name=dmRow2[db.sm_return_head.d_man_name.max()]
        retCount=dmRow2[db.sm_return_head.id.count()]
        retTpAmt=round(dmRow2[db.sm_return_head.total_amount.sum()]-dmRow2[db.sm_return_head.vat_total_amount.sum()]+dmRow2[db.sm_return_head.discount.sum()]+dmRow2[db.sm_return_head.sp_discount.sum()],2)
        retData={'d_man_id':d_man_id,'d_man_name':d_man_name,'invCount':0,'invTpAmt':0,'retCount':retCount,'retTpAmt':retTpAmt,'invData':'','retData':''}
        retList.append(retData)
    
    recordList=[]    
    for i in range(len(invList)):
        invDict=invList[i]
        d_man_id=invDict['d_man_id']
        
        ret_index=-1
        try:
            ret_index=str(map(itemgetter('d_man_id'), retList).index(d_man_id))    
        except:
            ret_index=-1
            
        if (ret_index!=-1):
            retDictData=retList[int(ret_index)]
            
            invDict['retCount']=str(retDictData['retCount'])
            invDict['retTpAmt']=str(retDictData['retTpAmt'])
            
            #recordList2.pop(ret_index)
            del retList[int(ret_index)]
    
    recordList=invList+retList    
    recordList.sort(key=itemgetter('d_man_id'), reverse=False) 
    
    #==========================================
    for m in range(len(recordList)):
        recordListStr=recordList[m]        
        d_man_id=recordListStr['d_man_id']
        
        dmDtailsList=[]        
        dmInvDetailsRows=db((db.sm_invoice_head.cid==c_id)&(db.sm_invoice_head.depot_id==depot_id)&(db.sm_invoice_head.store_id==store_id)&(db.sm_invoice_head.d_man_id==d_man_id)&(db.sm_invoice_head.invoice_date>=startDt)&(db.sm_invoice_head.invoice_date<=endDt)&(db.sm_invoice_head.status=='Invoiced')).select(db.sm_invoice_head.invoice_date,db.sm_invoice_head.depot_id,db.sm_invoice_head.sl,db.sm_invoice_head.actual_total_tp,orderby=db.sm_invoice_head.invoice_date)
        for dmDRow in dmInvDetailsRows:
            invoice_date=dmDRow.invoice_date
            depot_id=dmDRow.depot_id
            sl=dmDRow.sl
            actual_total_tp=dmDRow.actual_total_tp            
            dictDetailData={'invoice_date':invoice_date,'depot_id':depot_id,'sl':sl,'actual_total_tp':actual_total_tp}            
            dmDtailsList.append(dictDetailData)
        
        dmRetDtailsList=[]
        dmRetDetailsRows=db((db.sm_return_head.cid==c_id)&(db.sm_return_head.depot_id==depot_id)&(db.sm_return_head.store_id==store_id)&(db.sm_return_head.d_man_id==d_man_id)&(db.sm_return_head.return_date>=startDt)&(db.sm_return_head.return_date<=endDt)&(db.sm_return_head.status=='Returned')).select(db.sm_return_head.return_date,db.sm_return_head.invoice_sl,db.sm_return_head.invoice_date,db.sm_return_head.depot_id,db.sm_return_head.sl,db.sm_return_head.total_amount,db.sm_return_head.vat_total_amount,db.sm_return_head.discount,db.sm_return_head.sp_discount,orderby=db.sm_return_head.return_date)
        for dmRetDRow in dmRetDetailsRows:
            invoice_date=dmRetDRow.invoice_date
            return_date=dmRetDRow.return_date
            depot_id=dmRetDRow.depot_id
            sl=dmRetDRow.sl
            invoice_sl=dmRetDRow.invoice_sl
            total_amount=round(dmRetDRow.total_amount-dmRetDRow.vat_total_amount+dmRetDRow.discount+dmRetDRow.sp_discount,2)
            
            dictRetDetailData={'return_date':return_date,'sl':sl,'invoice_sl':invoice_sl,'invoice_date':invoice_date,'depot_id':depot_id,'total_amount':total_amount}            
            dmRetDtailsList.append(dictRetDetailData)
        
        recordListStr['invData']=dmDtailsList
        recordListStr['retData']=dmRetDtailsList
        
    return dict(recordList=recordList,date_from=startDt,date_to=endDt,depotName=depot_name,storeName=store_name,page=page,items_per_page=items_per_page)    


def dp_wise_doc_list_D():
    c_id=session.cid
    
    response.title='29 DP Wise Document List'
    
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
    
 
    invList=[]    
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.depot_id==depot_id)
    qset=qset(db.sm_invoice_head.store_id==store_id)
    qset=qset((db.sm_invoice_head.invoice_date>=startDt)&(db.sm_invoice_head.invoice_date<=endDt))
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    dMRecords=qset.select(db.sm_invoice_head.d_man_id,db.sm_invoice_head.d_man_name.max(),db.sm_invoice_head.id.count(),db.sm_invoice_head.actual_total_tp.sum(),groupby=db.sm_invoice_head.d_man_id)
    for dmRow in dMRecords:
        d_man_id=dmRow.sm_invoice_head.d_man_id
        d_man_name=dmRow[db.sm_invoice_head.d_man_name.max()]
        invCount=dmRow[db.sm_invoice_head.id.count()]
        invTpAmt=dmRow[db.sm_invoice_head.actual_total_tp.sum()]        
        invDPData={'d_man_id':d_man_id,'d_man_name':d_man_name,'invCount':invCount,'invTpAmt':invTpAmt,'retCount':0,'retTpAmt':0,'invData':'','retData':''}
        invList.append(invDPData)
        
    
    retList=[]
    qset2=db()
    qset2=qset2(db.sm_return_head.cid==c_id)
    qset2=qset2(db.sm_return_head.depot_id==depot_id)
    qset2=qset2(db.sm_return_head.store_id==store_id)
    qset2=qset2((db.sm_return_head.return_date>=startDt)&(db.sm_return_head.return_date<=endDt))
    qset2=qset2(db.sm_return_head.status=='Returned')
    dMRecords2=qset2.select(db.sm_return_head.d_man_id,db.sm_return_head.d_man_name.max(),db.sm_return_head.id.count(),db.sm_return_head.total_amount.sum(),db.sm_return_head.vat_total_amount.sum(),db.sm_return_head.discount.sum(),db.sm_return_head.sp_discount.sum(),groupby=db.sm_return_head.d_man_id)
    
    for dmRow2 in dMRecords2:
        d_man_id=dmRow2.sm_return_head.d_man_id
        d_man_name=dmRow2[db.sm_return_head.d_man_name.max()]
        retCount=dmRow2[db.sm_return_head.id.count()]
        retTpAmt=round(dmRow2[db.sm_return_head.total_amount.sum()]-dmRow2[db.sm_return_head.vat_total_amount.sum()]+dmRow2[db.sm_return_head.discount.sum()]+dmRow2[db.sm_return_head.sp_discount.sum()],2)
        retData={'d_man_id':d_man_id,'d_man_name':d_man_name,'invCount':0,'invTpAmt':0,'retCount':retCount,'retTpAmt':retTpAmt,'invData':'','retData':''}
        retList.append(retData)
    
    recordList=[]    
    for i in range(len(invList)):
        invDict=invList[i]
        d_man_id=invDict['d_man_id']
        
        ret_index=-1
        try:
            ret_index=str(map(itemgetter('d_man_id'), retList).index(d_man_id))    
        except:
            ret_index=-1
            
        if (ret_index!=-1):
            retDictData=retList[int(ret_index)]
            
            invDict['retCount']=str(retDictData['retCount'])
            invDict['retTpAmt']=str(retDictData['retTpAmt'])
            
            #recordList2.pop(ret_index)
            del retList[int(ret_index)]
    
    recordList=invList+retList    
    recordList.sort(key=itemgetter('d_man_id'), reverse=False) 
    
    #==========================================    
   
    for m in range(len(recordList)):
        recordListStr=recordList[m]        
        d_man_id=recordListStr['d_man_id']
        
        dmDtailsList=[]        
        dmInvDetailsRows=db((db.sm_invoice_head.cid==c_id)&(db.sm_invoice_head.depot_id==depot_id)&(db.sm_invoice_head.store_id==store_id)&(db.sm_invoice_head.d_man_id==d_man_id)&(db.sm_invoice_head.invoice_date>=startDt)&(db.sm_invoice_head.invoice_date<=endDt)&(db.sm_invoice_head.status=='Invoiced')).select(db.sm_invoice_head.invoice_date,db.sm_invoice_head.depot_id,db.sm_invoice_head.sl,db.sm_invoice_head.actual_total_tp,orderby=db.sm_invoice_head.invoice_date)
        for dmDRow in dmInvDetailsRows:
            invoice_date=dmDRow.invoice_date
            depot_id=dmDRow.depot_id
            sl=dmDRow.sl
            actual_total_tp=dmDRow.actual_total_tp            
            dictDetailData={'invoice_date':invoice_date,'depot_id':depot_id,'sl':sl,'actual_total_tp':actual_total_tp}            
            dmDtailsList.append(dictDetailData)
        
        dmRetDtailsList=[]
        dmRetDetailsRows=db((db.sm_return_head.cid==c_id)&(db.sm_return_head.depot_id==depot_id)&(db.sm_return_head.store_id==store_id)&(db.sm_return_head.d_man_id==d_man_id)&(db.sm_return_head.return_date>=startDt)&(db.sm_return_head.return_date<=endDt)&(db.sm_return_head.status=='Returned')).select(db.sm_return_head.return_date,db.sm_return_head.invoice_sl,db.sm_return_head.invoice_date,db.sm_return_head.depot_id,db.sm_return_head.sl,db.sm_return_head.total_amount,db.sm_return_head.vat_total_amount,db.sm_return_head.discount,db.sm_return_head.sp_discount,orderby=db.sm_return_head.return_date)
        for dmRetDRow in dmRetDetailsRows:
            invoice_date=dmRetDRow.invoice_date
            return_date=dmRetDRow.return_date
            depot_id=dmRetDRow.depot_id
            sl=dmRetDRow.sl
            invoice_sl=dmRetDRow.invoice_sl
            total_amount=round(dmRetDRow.total_amount-dmRetDRow.vat_total_amount+dmRetDRow.discount+dmRetDRow.sp_discount,2)
            
            dictRetDetailData={'return_date':return_date,'sl':sl,'invoice_sl':invoice_sl,'invoice_date':invoice_date,'depot_id':depot_id,'total_amount':total_amount}            
            dmRetDtailsList.append(dictRetDetailData)
        
        recordListStr['invData']=dmDtailsList
        recordListStr['retData']=dmRetDtailsList


    #=============== download
    myString='29 DP Wise Document List\n'
    
    myString+='Date From:,'+str(datetime.datetime.strptime(str(startDt),'%Y-%m-%d').strftime('%d-%b-%Y'))+'\n'
    myString+='Date To:,'+str(datetime.datetime.strptime(str(endDt),'%Y-%m-%d').strftime('%d-%b-%Y'))+'\n'
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depot_name)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(store_name)+'\n\n'  
    
    myString+='DP ID, Name,,Invoice Count, Invoice TP, Return Count, Return TP,Net'+'\n'
    
    for m in range(len(recordList)):
        dmInvListStr=recordList[m]
        d_man_id=dmInvListStr['d_man_id']
        d_man_name=dmInvListStr['d_man_name']
        invCount=dmInvListStr['invCount']
        invTpAmt=float(dmInvListStr['invTpAmt'])
        retCount=dmInvListStr['retCount']
        retTpAmt=float(dmInvListStr['retTpAmt'])
        netTp=float(dmInvListStr['invTpAmt'])-float(dmInvListStr['retTpAmt'])
        
        myString+=str(d_man_id)+','+str(d_man_name)+',,'+str(invCount)+','+str(invTpAmt)+','+str(retCount)+','+str(retTpAmt)+','+str(netTp)+',\n'
        
        dmDetailList=dmInvListStr['invData']
        for j in range(len(dmDetailList)):
            dmDetailStr=dmDetailList[j]
            invoice_date=dmDetailStr['invoice_date'].strftime('%d-%b-%Y')
            invoiceNo=session.prefix_invoice+'INV'+str(dmDetailStr['depot_id'])+'-'+str(dmDetailStr['sl'])
            actual_total_tp=float(dmDetailStr['actual_total_tp'])
            
            myString+=str(invoice_date)+','+str(invoiceNo)+',,,'+str(actual_total_tp)+',,,\n'
            
        dmRetDetailList=dmInvListStr['retData']
        for k in range(len(dmRetDetailList)):
            dmRetDetailStr=dmRetDetailList[k]
            return_date=dmRetDetailStr['return_date'].strftime('%d-%b-%Y')
            returnSl=session.prefix_invoice+'RET'+str(dmRetDetailStr['depot_id'])+'-'+str(dmRetDetailStr['sl'])
            refSl='Ref :'+session.prefix_invoice+'INV'+str(dmRetDetailStr['depot_id'])+'-'+str(dmRetDetailStr['invoice_sl'])
            refDate='Date '+str(dmRetDetailStr['invoice_date'].strftime('%d-%b-%Y')) 
            total_amount=str(float(dmRetDetailStr['total_amount']))       
            
            
            myString+=str(return_date)+','+str(returnSl)+','+str(refSl)+','+str(refDate)+',,,'+str(total_amount)+',\n'
        
    
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=dp_wise_doc_list_d.csv'   
    return str(myString)
    
    


def dp_wise_invoice_2():
    c_id=session.cid
    
    response.title='13 DP Wise Invoice 2'
    
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
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    

    dmInvList=[]
    
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.depot_id==depot_id)
    qset=qset(db.sm_invoice_head.store_id==store_id)
    qset=qset((db.sm_invoice_head.invoice_date>=startDt)&(db.sm_invoice_head.invoice_date<=endDt))
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    dMRecords=qset.select(db.sm_invoice_head.d_man_id,db.sm_invoice_head.d_man_name,db.sm_invoice_head.id.count(),db.sm_invoice_head.return_count.sum(),db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_sp_discount.sum(),groupby=db.sm_invoice_head.d_man_id|db.sm_invoice_head.d_man_name)
    
    
    for dmRow in dMRecords:
        d_man_id=dmRow.sm_invoice_head.d_man_id
        d_man_name=dmRow.sm_invoice_head.d_man_name
        invCount=dmRow[db.sm_invoice_head.id.count()]
        retCount=dmRow[db.sm_invoice_head.return_count.sum()]
        invTpAmt=dmRow[db.sm_invoice_head.actual_total_tp.sum()]
        returnTpAmt=dmRow[db.sm_invoice_head.return_tp.sum()]+dmRow[db.sm_invoice_head.return_sp_discount.sum()]
        
        dmInvData={'d_man_id':d_man_id,'d_man_name':d_man_name,'invCount':invCount,'retCount':retCount,'invTpAmt':invTpAmt,'returnTpAmt':returnTpAmt}
        dmInvList.append(dmInvData)    
        
        
    
    return dict(dmInvList=dmInvList,date_from=startDt,date_to=endDt,depotName=depot_name,storeName=store_name,page=page,items_per_page=items_per_page)    

def dp_wise_invoice_2_D():
    c_id=session.cid
    
    
    response.title='13 DP Wise Invoice 2'
    
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
    

    myString='13 DP Wise Invoice\n'
    
    myString+='Date From:,'+str(datetime.datetime.strptime(str(startDt),'%Y-%m-%d').strftime('%d-%b-%Y'))+'\n'
    myString+='Date To:,'+str(datetime.datetime.strptime(str(endDt),'%Y-%m-%d').strftime('%d-%b-%Y'))+'\n'
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depot_name)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(store_name)+'\n\n'
    
    
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.depot_id==depot_id)
    qset=qset(db.sm_invoice_head.store_id==store_id)
    qset=qset((db.sm_invoice_head.invoice_date>=startDt)&(db.sm_invoice_head.invoice_date<=endDt))
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    
    if startDt=='' and endDt=='':
        response.flash='Required Date From and Date To'        
    else:
        dMRecords=qset.select(db.sm_invoice_head.d_man_id,db.sm_invoice_head.d_man_name,db.sm_invoice_head.id.count(),db.sm_invoice_head.return_count.sum(),db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_sp_discount.sum(),groupby=db.sm_invoice_head.d_man_id|db.sm_invoice_head.d_man_name)
        
        myString+='DP ID, Name,Invoice TP, Return TP,Net'+'\n'
            
        dmInvDtailsList=[]
        for dmRow in dMRecords:
            d_man_id=dmRow.sm_invoice_head.d_man_id
            d_man_name=dmRow.sm_invoice_head.d_man_name
            invCount=dmRow[db.sm_invoice_head.id.count()]
            retCount=dmRow[db.sm_invoice_head.return_count.sum()]
            invTpAmt=dmRow[db.sm_invoice_head.actual_total_tp.sum()]
            returnTpAmt=dmRow[db.sm_invoice_head.return_tp.sum()]+dmRow[db.sm_invoice_head.return_sp_discount.sum()]
            
            myString+=str(d_man_id)+','+str(d_man_name)+','+str(invCount)+','+str(retCount)+',\n'            
            myString+=',,'+str(invTpAmt)+','+str(returnTpAmt)+','+str(invTpAmt-returnTpAmt)+'\n'
            

        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=dp_wise_invoice_2.csv'   
        return str(myString)


def dp_wise_invoice():
    c_id=session.cid
    
    response.title='13 DP Wise Invoice'
    
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
    qset=qset((db.sm_invoice_head.invoice_date>=startDt)&(db.sm_invoice_head.invoice_date<=endDt))
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    
    if startDt=='' and endDt=='':
        response.flash='Required Date From and Date To'        
    else:
        dMRecords=qset.select(db.sm_invoice_head.d_man_id,db.sm_invoice_head.d_man_name.max(),db.sm_invoice_head.id.count(),db.sm_invoice_head.return_count.sum(),db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_sp_discount.sum(),groupby=db.sm_invoice_head.d_man_id)
    
        dmInvList=[]
        dmInvDtailsList=[]
        for dmRow in dMRecords:
            d_man_id=dmRow.sm_invoice_head.d_man_id
            d_man_name=dmRow[db.sm_invoice_head.d_man_name.max()]
            invCount=dmRow[db.sm_invoice_head.id.count()]
            retCount=dmRow[db.sm_invoice_head.return_count.sum()]
            invTpAmt=dmRow[db.sm_invoice_head.actual_total_tp.sum()]
            returnTpAmt=dmRow[db.sm_invoice_head.return_tp.sum()]+dmRow[db.sm_invoice_head.return_sp_discount.sum()]
            
            
            dmInvDetailsRows=db((db.sm_invoice_head.cid==c_id)&(db.sm_invoice_head.depot_id==depot_id)&(db.sm_invoice_head.store_id==store_id)&(db.sm_invoice_head.d_man_id==d_man_id)&(db.sm_invoice_head.invoice_date>=startDt)&(db.sm_invoice_head.invoice_date<=endDt)).select(db.sm_invoice_head.invoice_date,db.sm_invoice_head.depot_id,db.sm_invoice_head.sl,db.sm_invoice_head.actual_total_tp,db.sm_invoice_head.return_tp,db.sm_invoice_head.return_sp_discount,orderby=db.sm_invoice_head.invoice_date)
            
            for dmDRow in dmInvDetailsRows:
                invoice_date=dmDRow.invoice_date
                depot_id=dmDRow.depot_id
                sl=dmDRow.sl
                a_tp_amount=dmDRow.actual_total_tp
                return_tp=dmDRow.return_tp+dmDRow.return_sp_discount
                
                dictDetailData={'invoice_date':invoice_date,'depot_id':depot_id,'sl':sl,'a_tp_amount':a_tp_amount,'return_tp':return_tp}            
                dmInvDtailsList.append(dictDetailData)
            
            dmInvData={'d_man_id':d_man_id,'d_man_name':d_man_name,'invCount':invCount,'retCount':retCount,'invTpAmt':invTpAmt,'returnTpAmt':returnTpAmt,'dmInvDtailsList':dmInvDtailsList}
            dmInvList.append(dmInvData)    
        
        
    
    return dict(dmInvList=dmInvList,date_from=startDt,date_to=endDt,depotName=depot_name,storeName=store_name,page=page,items_per_page=items_per_page)    

def dp_wise_invoice_D():
    c_id=session.cid
    
    
    response.title='13 DP Wise Invoice'
    
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
    

    myString='13 DP Wise Invoice\n'
    
    myString+='Date From:,'+str(datetime.datetime.strptime(str(startDt),'%Y-%m-%d').strftime('%d-%b-%Y'))+'\n'
    myString+='Date To:,'+str(datetime.datetime.strptime(str(endDt),'%Y-%m-%d').strftime('%d-%b-%Y'))+'\n'
    myString+='Branch ID:,'+str(depot_id)+'\n'
    myString+='Branch Name'+','+str(depot_name)+'\n'
    myString+='Store ID:,'+str(store_id)+'\n'
    myString+='Store Name'+','+str(store_name)+'\n\n'
    
    
    dmInvList=[]
    
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.depot_id==depot_id)
    qset=qset(db.sm_invoice_head.store_id==store_id)
    qset=qset((db.sm_invoice_head.invoice_date>=startDt)&(db.sm_invoice_head.invoice_date<=endDt))
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    
    if startDt=='' and endDt=='':
        response.flash='Required Date From and Date To'        
    else:
        dMRecords=qset.select(db.sm_invoice_head.d_man_id,db.sm_invoice_head.d_man_name.max(),db.sm_invoice_head.id.count(),db.sm_invoice_head.return_count.sum(),db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_sp_discount.sum(),groupby=db.sm_invoice_head.d_man_id)
        
        myString+='DP ID, Name,Invoice TP, Return TP,Net'+'\n'
            
        dmInvDtailsList=[]
        for dmRow in dMRecords:
            d_man_id=dmRow.sm_invoice_head.d_man_id
            d_man_name=dmRow[db.sm_invoice_head.d_man_name.max()]
            invCount=dmRow[db.sm_invoice_head.id.count()]
            retCount=dmRow[db.sm_invoice_head.return_count.sum()]
            invTpAmt=dmRow[db.sm_invoice_head.actual_total_tp.sum()]
            returnTpAmt=dmRow[db.sm_invoice_head.return_tp.sum()]+dmRow[db.sm_invoice_head.return_sp_discount.sum()]
            
            myString+=str(d_man_id)+','+str(d_man_name)+','+str(invCount)+','+str(retCount)+',\n'            
            myString+=',,'+str(invTpAmt)+','+str(returnTpAmt)+','+str(invTpAmt-returnTpAmt)+'\n'
            
            dmInvDetailsRows=db((db.sm_invoice_head.cid==c_id)&(db.sm_invoice_head.depot_id==depot_id)&(db.sm_invoice_head.store_id==store_id)&(db.sm_invoice_head.d_man_id==d_man_id)&(db.sm_invoice_head.invoice_date>=startDt)&(db.sm_invoice_head.invoice_date<=endDt)).select(db.sm_invoice_head.invoice_date,db.sm_invoice_head.depot_id,db.sm_invoice_head.sl,db.sm_invoice_head.actual_total_tp,db.sm_invoice_head.return_tp,db.sm_invoice_head.return_sp_discount,orderby=db.sm_invoice_head.invoice_date)
            
            for dmDRow in dmInvDetailsRows:
                invoice_date=dmDRow.invoice_date
                depot_id=dmDRow.depot_id
                sl=dmDRow.sl
                a_tp_amount=dmDRow.actual_total_tp
                return_tp=dmDRow.return_tp+dmDRow.return_sp_discount
                
                myString+=str(invoice_date)+','+str(session.prefix_invoice)+'INV'+str(depot_id)+'-'+str(sl)+','+str(a_tp_amount)+','+str(return_tp)+','+str(a_tp_amount-return_tp)+'\n'
            

        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=dp_wise_invoice.csv'   
        return str(myString)
       
            
       