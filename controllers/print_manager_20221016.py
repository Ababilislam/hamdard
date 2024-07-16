import urllib2
from operator import itemgetter

#======================= Print Invoice List
def print_invoice():
    c_id=session.cid
    
    #----------------
    response.title='Print-Invoice/Delivery'
    #Check access permission
    #----------Task assaign----------
    task_id='rm_print_manager_view'
    access_permission=check_role(task_id)
    if (access_permission==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
        
    #Set text for filter    
    btn_filter_printm=request.vars.btn_filter
    btn_all=request.vars.btn_all
    
    currentDate=current_date
    submitFlag=1
    pageBreakFlag=1
    
    search_type=str(request.vars.search_type).strip()
    search_value=str(request.vars.search_value).strip()
    search_dt=str(request.vars.from_dt).strip()
    search_delivery=str(request.vars.search_delivery).strip()    
    print_status=str(request.vars.print_status).strip()
    limitOver=str(request.vars.limitOver).strip()
    emptyBatch=str(request.vars.emptyBatch).strip()
    paymentMode=str(request.vars.paymentMode).strip()
    
    reqPage=len(request.args)
    # Set sessions for filter
    if btn_filter_printm:
        session.btn_filter_printm=btn_filter_printm        
        session.search_type_printm=search_type
        session.search_value_printm=search_value
        session.search_delivery=search_delivery
        session.print_status=print_status
        session.limitOver=limitOver
        session.emptyBatch=emptyBatch
        session.paymentMode=paymentMode
        
        # Check SL is integer or not
        if (session.search_type_printm=='SL'):
            sl=0
            if not(session.search_value_printm=='' or session.search_value_printm==None):
                try:
                    sl=int(session.search_value_printm)
                    session.search_value_printm=sl
                except:
                    session.search_value_printm=sl
                    response.flash='sl needs number value'
            else:
                session.search_value_printm=sl
                
        #---
        try:
            currentDate=datetime.datetime.strptime(search_dt,'%Y-%m-%d').strftime('%Y-%m-%d')
            session.search_dt=currentDate
        except:
            session.search_dt=''
            
        reqPage=0
        
    elif btn_all:
        session.btn_filter_printm=None
        session.print_status=None
        session.search_type_printm=None
        session.search_value_printm=None
        session.search_dt=None        
        session.search_delivery=None
        session.limitOver=None   
        session.emptyBatch=None   
        session.paymentMode=None
        reqPage=0
        
    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=25   #session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging  
    
    # Set query based on search type
    deliveryManRows =''
    shipmentRows =''
    records=''
    totalRecords=0
    totalCount=0
    
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.sl!=0)
    qset=qset(db.sm_invoice_head.status=='Submitted')
    
    if (session.user_type=='Depot'):
        qset=qset(db.sm_invoice_head.depot_id==session.depot_id)
        
        if (session.search_dt=='' or session.search_dt==None):  # Not filter
            qset=qset(db.sm_invoice_head.delivery_date<=currentDate)                  
        else:
            #----------
            if session.search_delivery=='UptoDelDate':
                qset=qset(db.sm_invoice_head.delivery_date<=session.search_dt) 
                    
            elif session.search_delivery=='OnDelDate':
                qset=qset(db.sm_invoice_head.delivery_date==session.search_dt)
                
        if (session.btn_filter_printm):            
            #------------
            if (session.search_type_printm=='SL'):
                qset=qset(db.sm_invoice_head.sl==session.search_value_printm)
                
            elif (session.search_type_printm=='REPID'):                
                searchValue=str(session.search_value_printm).split('|')[0]
                qset=qset(db.sm_invoice_head.rep_id==searchValue)
                
            elif (session.search_type_printm=='ORDSL'):                
                try:
                    order_sl=int(session.search_value_printm)
                except:
                    order_sl=None
                qset=qset(db.sm_invoice_head.order_sl==order_sl)
                
            elif (session.search_type_printm=='ROUTEID'):
                searchValue=str(session.search_value_printm).split('|')[0]
                qset=qset(db.sm_invoice_head.area_id==searchValue)
                
            
            elif (session.search_type_printm=='CLIENTID'):
                searchValue=str(session.search_value_printm).split('|')[0]
                qset=qset(db.sm_invoice_head.client_id==searchValue)
            
            elif (session.search_type_printm=='DPID'):
                searchValue=str(session.search_value_printm).split('|')[0].upper()
                qset=qset(db.sm_invoice_head.d_man_id==searchValue)
                
            elif (session.search_type_printm=='ORDDATE'):
                try:
                    order_datetimeFrom=datetime.datetime.strptime(str(session.search_value_printm),'%Y-%m-%d')
                    order_datetimeTo=order_datetimeFrom+datetime.timedelta(days=1)
                except:
                    order_datetimeFrom=''
                    order_datetimeTo=''
                qset=qset((db.sm_invoice_head.order_datetime>=order_datetimeFrom)&(db.sm_invoice_head.order_datetime<order_datetimeTo))
            
            #----------
            if session.print_status=='Pending':
                qset=qset(db.sm_invoice_head.field2==0)
            
            #----------
            if session.paymentMode!='':
                qset=qset(db.sm_invoice_head.payment_mode==session.paymentMode)
            
            #----------
            if (session.limitOver!=''):
                qset=qset(db.sm_invoice_head.client_limit_over==session.limitOver)
            
            #----------
            if (session.emptyBatch!=''):
                qset=qset(db.sm_invoice_head.empty_batch_flag==session.emptyBatch)
                
        if submitFlag==1:
            records=qset.select(db.sm_invoice_head.ALL,orderby=~db.sm_invoice_head.sl,limitby=limitby)
            deliveryManRows = db((db.sm_delivery_man.cid == c_id) & (db.sm_delivery_man.depot_id == session.depot_id)& (db.sm_delivery_man.status=='ACTIVE')).select(db.sm_delivery_man.d_man_id, db.sm_delivery_man.name, orderby=db.sm_delivery_man.name)
            
        else:
            records=qset.select(db.sm_invoice_head.ALL,orderby=~db.sm_invoice_head.sl,limitby=limitby)
        
        totalRecords=len(records)
            
            
    else:
        records=''
        response.flash='Only depot user can print'
    
    totalCount=qset.count()
    
    #------------ filter form
    filterform =SQLFORM(db.sm_search_date,
                  fields=['from_dt']
                  )
    
    if (session.search_dt=='' or session.search_dt==None):
        #session.search_delivery='UptoDelDate'
        filterform.vars.from_dt=currentDate
    else:
        filterform.vars.from_dt=session.search_dt
        
    if filterform.accepts(request.vars,session):
        pass
    
    invoiceTermRows=db((db.sm_category_type.cid==session.cid) & (db.sm_category_type.type_name=='PAYMENT_MODE')).select(db.sm_category_type.cat_type_id,orderby=db.sm_category_type.cat_type_id)
    
    shipmentRows=[]#db((db.sm_invoice_head.cid==c_id)&(db.sm_invoice_head.depot_id==session.depot_id)&(db.sm_invoice_head.invoice_date==current_date)&(db.sm_invoice_head.shipment_no!='')).select(db.sm_invoice_head.shipment_no,orderby=~db.sm_invoice_head.shipment_no,groupby=db.sm_invoice_head.shipment_no)
    
    return dict(records=records,shipmentRows=shipmentRows,filterform=filterform,currentDate=currentDate,totalRecords=totalRecords,totalCount=totalCount,invoiceTermRows=invoiceTermRows,submitFlag=submitFlag,pageBreakFlag=pageBreakFlag,deliveryManRows=deliveryManRows,page=page,items_per_page=items_per_page,access_permission=access_permission)
    
def invoice_list_post():
    c_id=session.cid
    req_depot=session.depot_id
    
    btn_print_submit=request.vars.btn_print_submit
    btn_confirm_post=request.vars.btn_confirm_post
    
    #req_date=request.vars.invoice_date
    d_man_id=request.vars.d_man_id
    shipment_no=request.vars.shipment_no
    if shipment_no=='' or shipment_no==None:
        shipment_no=str(date_fixed)[0:16].replace('-','').replace(':','').replace(' ','-')+str(date_fixed.strftime('%p'))
        
        newExist=db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==req_depot) &(db.sm_invoice_head.invoice_date==current_date) &(db.sm_invoice_head.shipment_no==shipment_no)).select(db.sm_invoice_head.id,limitby=(0,1))
        if newExist:
            session.flash='Shipment no error, please try again after 1 minute'
            redirect('print_invoice')
            
    #else:
        #d_man_id=str(shipment_no).split('-')[1]
        
    req_date=current_date
    ym_date=str(req_date)[0:7]+'-01'
    
    vslList=[]
    vslList=request.vars.vslList
    
    if vslList==None or vslList=='0':
        session.flash='need select voucher'
    else:
#         if btn_print_submit:
#             redirect(URL(c='print_manager',f='invoice_list_preview',vars=dict(vslList=vslList)))
        
        if btn_confirm_post:
            if req_date=='':
                session.flash='Required Invoice Date'
            else:
                if d_man_id=='':
                    session.flash='Required Delivery Man'
                else:
                    slList=[]
                    for i in range(len(vslList)):
                        reqSl=str(vslList[i]).strip()        
                        if reqSl=='0':            
                            continue
                        else:
                            slList.append(reqSl)
                    #------------------
                    headSubmit=db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==req_depot) & (db.sm_invoice_head.sl.belongs(slList))& (db.sm_invoice_head.status!='Submitted')).select(db.sm_invoice_head.id,limitby=(0,1))
                    if headSubmit:
                        session.flash='Required only Submitted record'
                    else:                        
                        headAcknowledge=db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==req_depot) & (db.sm_invoice_head.sl.belongs(slList))& (db.sm_invoice_head.acknowledge_flag=='1')).select(db.sm_invoice_head.id,db.sm_invoice_head.acknowledge_flag,limitby=(0,1))
                        if headAcknowledge:
                            session.flash='Required Acknowledgement'
                        else:                            
                            batchIdrows=db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==req_depot) & (db.sm_invoice.sl.belongs(slList)) & (db.sm_invoice.batch_id=='')).select(db.sm_invoice.id,limitby=(0,1))
                            if batchIdrows:
                                session.flash = 'Required Batch ID for all Items'                                
                            else:                                
                                d_man_name=''
                                dmanRecords=db((db.sm_delivery_man.cid==c_id)& (db.sm_delivery_man.depot_id==req_depot) & (db.sm_delivery_man.d_man_id==d_man_id)).select(db.sm_delivery_man.id,db.sm_delivery_man.name,limitby=(0,1))
                                if dmanRecords:
                                    d_man_name=dmanRecords[0].name
                                    
                                #--------------------------- chcek stock cron flag
                                autDelCronRows=db((db.sm_depot.cid==c_id)&(db.sm_depot.depot_id==req_depot)&(db.sm_depot.auto_del_cron_flag==0)).select(db.sm_depot.id,db.sm_depot.cid,limitby=(0,1))
                                if not autDelCronRows:
                                    session.flash='One process running, please try again'
                                else:
                                    autDelCronRows[0].update_record(auto_del_cron_flag=1)
                                    #---------------------
                                    
                                    declaredItemList=[]
                                    declaredItemRows=db((db.sm_promo_declared_item.cid==c_id)&(db.sm_promo_declared_item.status=='ACTIVE')).select(db.sm_promo_declared_item.product_id)
                                    for decRow in declaredItemRows:
                                        declaredItemList.append(decRow.product_id)
                                    #------------
                                    
                                    req_sl=0
                                    count=0
                                    errorStr=''
                                    for j in range(len(slList)):
                                        req_sl=str(slList[j]).strip() 
                                        
                                        #-------------------------------- Loop start
                                        headRow=db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==req_depot) & (db.sm_invoice_head.sl==req_sl)& (db.sm_invoice_head.status=='Submitted')).select(db.sm_invoice_head.id,db.sm_invoice_head.sl,db.sm_invoice_head.d_man_id,db.sm_invoice_head.d_man_name,db.sm_invoice_head.shipment_no,db.sm_invoice_head.order_sl,db.sm_invoice_head.updated_by,db.sm_invoice_head.depot_id,db.sm_invoice_head.store_id,db.sm_invoice_head.client_id,db.sm_invoice_head.area_id,db.sm_invoice_head.discount,db.sm_invoice_head.sp_discount,db.sm_invoice_head.depot_name,db.sm_invoice_head.store_name,db.sm_invoice_head.delivery_date,db.sm_invoice_head.payment_mode,db.sm_invoice_head.credit_note,db.sm_invoice_head.client_name,db.sm_invoice_head.rep_id,db.sm_invoice_head.rep_name,db.sm_invoice_head.market_id,db.sm_invoice_head.market_name,db.sm_invoice_head.level0_id,db.sm_invoice_head.level0_name,db.sm_invoice_head.level1_id,db.sm_invoice_head.level1_name,db.sm_invoice_head.level2_id,db.sm_invoice_head.level2_name,db.sm_invoice_head.area_name,db.sm_invoice_head.note,db.sm_invoice_head.posted_by,limitby=(0,1))
                                        if not headRow:
                                            errorStr= 'Invalid SL no '+str(req_sl)
                                        else:
                                            inv_rowid = headRow[0].id
                                            store_id=headRow[0].store_id
                                            client_id=headRow[0].client_id
                                            area_id=headRow[0].area_id
                                            discount=float(headRow[0].discount)

                                            # --------------------- for transaction report
                                            depot_name = headRow[0].depot_name
                                            store_name = headRow[0].store_name
                                            delivery_date = headRow[0].delivery_date
                                            payment_mode = headRow[0].payment_mode
                                            credit_note = headRow[0].credit_note
                                            client_name = headRow[0].client_name
                                            rep_id = headRow[0].rep_id
                                            rep_name = headRow[0].rep_name
                                            market_id = headRow[0].market_id
                                            market_name = headRow[0].market_name
                                            level0_id = headRow[0].level0_id
                                            level0_name = headRow[0].level0_name
                                            level1_id = headRow[0].level1_id
                                            level1_name = headRow[0].level1_name
                                            level2_id = headRow[0].level2_id
                                            level2_name = headRow[0].level2_name
                                            area_name = headRow[0].area_name
                                            note = headRow[0].note
                                            posted_by = headRow[0].posted_by
                                            
                                            itemStrForQty=''  
                                            diffRecords="select inv.item_id as item_id from sm_depot_stock_balance dsb,(select invtemp.cid as cid,invtemp.depot_id as depot_id,invtemp.sl as sl,invtemp.store_id as store_id,invtemp.item_id as item_id,invtemp.batch_id as batch_id,sum(invtemp.quantity) as quantity,sum(invtemp.bonus_qty) as bonus_qty from sm_invoice invtemp where (invtemp.cid='"+str(c_id)+"' and invtemp.depot_id='"+str(req_depot)+"' and invtemp.sl="+str(req_sl)+" and invtemp.store_id='"+str(store_id)+"') group by invtemp.cid,invtemp.depot_id,invtemp.sl,invtemp.store_id,invtemp.item_id,invtemp.batch_id) inv  where (inv.cid='"+str(c_id)+"' and inv.depot_id='"+str(req_depot)+"' and inv.sl="+str(req_sl)+" and inv.store_id='"+str(store_id)+"' and dsb.cid='"+str(c_id)+"' and dsb.depot_id='"+str(req_depot)+"' and dsb.store_id='"+str(store_id)+"' and inv.item_id=dsb.item_id and inv.batch_id=dsb.batch_id and (dsb.quantity)<(inv.quantity+inv.bonus_qty))"
                                            
                                            #diffRecords="select inv.item_id as item_id from sm_depot_stock_balance dsb,sm_invoice inv  where (inv.cid='"+str(c_id)+"' and inv.depot_id='"+str(req_depot)+"' and inv.sl="+str(req_sl)+" and dsb.cid='"+str(c_id)+"' and dsb.depot_id='"+str(req_depot)+"' and inv.store_id=dsb.store_id and inv.item_id=dsb.item_id and inv.batch_id=dsb.batch_id and (dsb.quantity-dsb.block_qty)<inv.quantity+inv.bonus_qty)"
                                            diffRowsList=db.executesql(diffRecords,as_dict=True)
                                            for i in range(len(diffRowsList)):
                                                diffDictData=diffRowsList[i]
                                                if itemStrForQty=='':
                                                    itemStrForQty=diffDictData['item_id']
                                                else:
                                                    itemStrForQty+=','+diffDictData['item_id']
                                                    
                                            if itemStrForQty!='':
                                                errorStr='Quantity not available for item ID '+str(itemStrForQty)+' of Invoice SL'+str(req_sl)
                                            else:
                                                cl_category_id=''
                                                cl_category_name=''
                                                cl_sub_category_id=''
                                                cl_sub_category_name=''
                                                clientRow=db((db.sm_client.cid==c_id)& (db.sm_client.depot_id==req_depot) & (db.sm_client.client_id==client_id)).select(db.sm_client.category_id,db.sm_client.category_name,db.sm_client.sub_category_id,db.sm_client.sub_category_name,limitby=(0,1))
                                                if clientRow:
                                                    cl_category_id=clientRow[0].category_id
                                                    cl_category_name=clientRow[0].category_name
                                                    cl_sub_category_id=clientRow[0].sub_category_id
                                                    cl_sub_category_name=clientRow[0].sub_category_name
                                                
                                                special_territory_code=''
                                                levelRow=db((db.sm_level.cid==c_id)& (db.sm_level.level_id==area_id)).select(db.sm_level.special_territory_code,limitby=(0,1))
                                                if levelRow:
                                                    special_territory_code=levelRow[0].special_territory_code                                                
                                                    
                                                #osRows=db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==req_depot) & (db.sm_invoice_head.sl<req_sl) & (db.sm_invoice_head.client_id==client_id) & (db.sm_invoice_head.status=='Invoiced') & ((db.sm_invoice_head.total_amount-(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat-db.sm_invoice_head.return_discount)) > db.sm_invoice_head.collection_amount)).select(db.sm_invoice_head.ALL,orderby=~db.sm_invoice_head.id)
                                                #prevReceivableTotal=0
                                                #for osRow in osRows:
                                                    #recInvTotal=osRow.total_amount-(osRow.return_tp+osRow.return_vat-osRow.return_discount)
                                                    #prevReceivableTotal+=(recInvTotal-osRow.collection_amount)
                                                    
                                                previous_ost_amt=0
                                                osSql="select SUM(total_amount-(return_tp+return_vat-return_discount)-collection_amount) as prevOSAmt from sm_invoice_head where cid='"+str(c_id)+"' and depot_id='"+str(req_depot)+"' and sl!='"+str(req_sl)+"' and client_id='"+str(client_id)+"' and status='Invoiced' and round(total_amount-(return_tp+return_vat-return_discount),2)>round(collection_amount,2) group by client_id"
                                                osRecordsList=db.executesql(osSql,as_dict = True)
                                                for k in range(len(osRecordsList)):
                                                    previous_ost_amt=round(osRecordsList[k]['prevOSAmt'],2)
                                                    break
                                                    
                                                client_limit_amt=''
                                                creditRow=db((db.sm_cp_approved.cid==c_id)& (db.sm_cp_approved.client_id==client_id) & (db.sm_cp_approved.status=='ACTIVE')).select(db.sm_cp_approved.credit_amount,limitby=(0,1))
                                                if creditRow:
                                                    client_limit_amt=creditRow[0].credit_amount
                                                    
                                                #---------------------
                                                totalAmount=0
                                                total_tp_amount=0
                                                total_vat_amount=0
                                                sp_discount=0
                                                sp_flat=0
                                                sp_approved=0
                                                sp_others=0
                                                actual_total_tp=0
                                                total_tp_discount=0
                                                
                                                regular_disc_tp=0   #actual total tp-regular
                                                flat_disc_tp=0      #actual total tp-flat
                                                approved_disc_tp=0  #actual total tp-approved
                                                others_disc_tp=0    #actual total tp-others
                                                no_disc_tp=0        #actual total tp-no disc
                                                
                                                rows=db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==req_depot) & (db.sm_invoice.sl==req_sl) & (db.sm_invoice.quantity!=0)  & (db.sm_invoice.status=='Submitted')).select(db.sm_invoice.id,db.sm_invoice.item_id,db.sm_invoice.actual_tp,db.sm_invoice.quantity,db.sm_invoice.price,db.sm_invoice.item_vat,db.sm_invoice.promotion_type,db.sm_invoice.short_note)
                                                for row in rows:
                                                    itemId=row.item_id
                                                    actual_tp=float(row.actual_tp)
                                                    quantity=int(row.quantity)
                                                    price=float(row.price)
                                                    item_vat=float(row.item_vat)
                                                    short_note=str(row.short_note).upper()
                                                    promotion_type=str(row.promotion_type).upper()
                                                    
                                                    # not for bonus item
                                                    itemActualTp=round(quantity*actual_tp,6)
                                                                 
                                                    actual_total_tp+=itemActualTp                                         
                                                    total_tp_amount+=round(quantity*price,6)
                                                    total_vat_amount+=round(quantity*item_vat,6)
                                                    
                                                    discountType=''
                                                    itemDiscount=0
                                                    spDiscount=actual_tp-price
                                                    item_discount_percent=0
                                                    discount_type_quantity=0
                                                    
                                                    if spDiscount!=0:
                                                        #special Discount
                                                        #discountType='SP'
                                                        discount_type_quantity=quantity
                                                        itemDiscount=round(spDiscount*quantity,2)
                                                        sp_discount+=itemDiscount                                                        
                                                        item_discount_percent=round((spDiscount*100)/actual_tp,2)  #discount percent on actual tp                                                      
                                                        if promotion_type=='FLAT':
                                                            discountType='FLAT'
                                                            sp_flat+=itemDiscount
                                                            flat_disc_tp+=itemActualTp
                                                            
                                                        elif promotion_type=='APPROVED':
                                                            discountType='APPROVED'
                                                            sp_approved+=itemDiscount
                                                            approved_disc_tp+=itemActualTp
                                                                                              
                                                        else:
                                                            discountType='OTHERS'
                                                            sp_others+=itemDiscount
                                                            others_disc_tp+=itemActualTp
                                                                  
                                                    else:
                                                        if itemId in declaredItemList:
                                                            #declared item
                                                            pass
                                                        else:#regular discount            
                                                            if discount==0:
                                                                pass
                                                            else:
                                                                if short_note.find('REGULAR DISCOUNT')!=-1:
                                                                    discountType='RD'
                                                                    rdQuantity=quantity
                                                                    
                                                                    #----
                                                                    rdQtyindex1=short_note.find('REGULAR DISCOUNT ON')
                                                                    if (rdQtyindex1!=-1):
                                                                        rdQtyindex2=short_note.find('QUANTITY')
                                                                        try:
                                                                            disQty=int(short_note[(rdQtyindex1+19):rdQtyindex2])
                                                                        except:
                                                                            disQty=0
                                                                        
                                                                        if disQty!=0:
                                                                            rdQuantity=disQty
                                                                        
                                                                    #----------
                                                                    discount_type_quantity=rdQuantity
                                                                    total_tp_discount+=round(rdQuantity*price,6)
                                                                    regular_disc_tp+=round(rdQuantity*actual_tp,6)
                                                                    
                                                    #----------
                                                    row.update_record(sp_discount_item=itemDiscount,discount_type=discountType,item_discount=itemDiscount,item_discount_percent=item_discount_percent,discount_type_quantity=discount_type_quantity)
                                                        
                                                #---------Regular discount distribution update
                                                rows2=db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==req_depot) & (db.sm_invoice.sl==req_sl) & (db.sm_invoice.quantity!=0) & (db.sm_invoice.status=='Submitted') & (db.sm_invoice.discount_type=='RD')).select(db.sm_invoice.id,db.sm_invoice.quantity,db.sm_invoice.price,db.sm_invoice.short_note)
                                                for row2 in rows2:
                                                    quantity2=int(row2.quantity)
                                                    price2=float(row2.price)
                                                    short_note2=str(row2.short_note).upper()
                                                    rdQuantity=quantity2
                                                    
                                                    rdQtyindex1=short_note2.find('REGULAR DISCOUNT ON')
                                                    if rdQtyindex1!=-1:
                                                        rdQtyindex2=short_note2.find('QUANTITY')
                                                        try:
                                                            disQty=int(str(short_note2[(rdQtyindex1+19):rdQtyindex2]).strip())
                                                        except:
                                                            disQty=0
                                                        
                                                        if disQty!=0:
                                                            rdQuantity=disQty
                                                            
                                                    dis_tp_amt=round(rdQuantity*price2,6)
                                                    
                                                    itemDiscount=round((dis_tp_amt*discount)/total_tp_discount,2)
                                                    
                                                    item_discount_percent=round((itemDiscount*100)/dis_tp_amt,2)
                                                    
                                                    row2.update_record(item_discount=itemDiscount,item_discount_percent=item_discount_percent)
                                                    
                                                #-------------
                                                totalAmount=round((round(total_tp_amount,2)+round(total_vat_amount,2)-round(discount,2)),2) #with vat
                                                total_vat_amount=round(total_vat_amount,2)
                                                sp_discount=round(sp_discount,2)
                                                actual_total_tp=round(actual_total_tp,2)
                                                
                                                regular_disc_tp=round(regular_disc_tp,2)
                                                flat_disc_tp=round(flat_disc_tp,2)
                                                approved_disc_tp=round(approved_disc_tp,2)
                                                others_disc_tp=round(others_disc_tp,2)
                                                no_disc_tp=round(actual_total_tp-(regular_disc_tp+flat_disc_tp+approved_disc_tp+others_disc_tp),2)
                                                
                                                sp_flat=round(sp_flat,2)
                                                sp_approved=round(sp_approved,2)
                                                sp_others=round(sp_others,2)

                                                # distributor discount
                                                dist_disc_percent = 0
                                                distDiscRows = "select dist_disc_percent from sm_depot_distributor where cid='" + c_id + "' and depot_id='" + req_depot + "' limit 0,1;"
                                                distDiscRows = db.executesql(distDiscRows, as_dict=True)

                                                dist_discount = 0
                                                for j in range(len(distDiscRows)):
                                                    distDiscRowsS = distDiscRows[j]
                                                    dist_disc_percent = distDiscRowsS['dist_disc_percent']

                                                dist_discount = actual_total_tp * dist_disc_percent / 100
                                                dist_discount = round(float(dist_discount), 2)
                                                
                                                #Create string for balance return function                
                                                if session.ledgerCreate=='YES':                    
                                                    strData=str(c_id)+'<fdfd>DELIVERY<fdfd>'+str(req_sl)+'<fdfd>'+str(datetime_fixed)+'<fdfd>'+str(req_depot)+'-'+str(req_sl)+'<fdfd>DPT-'+str(req_depot)+'<fdfd>CLT-'+str(client_id)+'<fdfd>'+str(totalAmount)
                                                    resStr=set_balance_transaction(strData)
                                                    resStrList=resStr.split('<sep>',resStr.count('<sep>'))
                                                    flag=resStrList[0]
                                                    msg=resStrList[1]
                                                else:
                                                    flag='True'
                                                    msg='Success'
                                                    
                                                if flag=='True':
                                                    #Update status of head and detail                                            
                                                    db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==req_depot) & (db.sm_invoice.sl==req_sl)).update(status='Invoiced',d_man_id=d_man_id,d_man_name=d_man_name,invoice_date=req_date,invoice_ym_date=ym_date,cl_category_id=cl_category_id,cl_category_name=cl_category_name,cl_sub_category_id=cl_sub_category_id,cl_sub_category_name=cl_sub_category_name,special_territory_code=special_territory_code,posted_on=date_fixed,posted_by=session.user_id)
                                                    db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==req_depot) & (db.sm_invoice_head.sl==req_sl)).update(status='Invoiced',invoice_date=req_date,invoice_ym_date=ym_date,d_man_id=d_man_id,d_man_name=d_man_name,actual_total_tp=actual_total_tp,regular_disc_tp=regular_disc_tp,flat_disc_tp=flat_disc_tp,approved_disc_tp=approved_disc_tp,others_disc_tp=others_disc_tp,no_disc_tp=no_disc_tp,total_amount=totalAmount,vat_total_amount=total_vat_amount,sp_discount=sp_discount,sp_flat=sp_flat,sp_approved=sp_approved,sp_others=sp_others,previous_ost_amt=previous_ost_amt,client_limit_amt=client_limit_amt,empty_batch_flag=0,shipment_no=shipment_no,cl_category_id=cl_category_id,cl_category_name=cl_category_name,cl_sub_category_id=cl_sub_category_id,cl_sub_category_name=cl_sub_category_name,special_territory_code=special_territory_code,rpt_trans_flag=1,posted_on=date_fixed,posted_by=session.user_id,dist_discount=dist_discount)

                                                    # ----------------------- Report Transaction ***
                                                    transaction_date = current_date
                                                    insertRpt = db.sm_rpt_transaction.insert(cid=c_id,depot_id=req_depot,depot_name=depot_name,store_id=store_id,store_name=store_name,inv_rowid=inv_rowid,inv_sl=req_sl,invoice_date=req_date,transaction_type='INV',transaction_date=transaction_date,transaction_ref=req_sl,transaction_ref_date=req_date,trans_net_amt=totalAmount,tp_amt=actual_total_tp,vat_amt=total_vat_amount,disc_amt=round(discount,2),spdisc_amt=sp_discount,adjust_amount=0,delivery_date=delivery_date,payment_mode=payment_mode,credit_note=credit_note,client_id=client_id,client_name=client_name,cl_category_id=cl_category_id,cl_category_name=cl_category_name,cl_sub_category_id=cl_sub_category_id,cl_sub_category_name=cl_sub_category_name,client_limit_amt=client_limit_amt,rep_id=rep_id,rep_name=rep_name,market_id=market_id,market_name=market_name,d_man_id=d_man_id,d_man_name=d_man_name,level0_id=level0_id,level0_name=level0_name,level1_id=level1_id,level1_name=level1_name,level2_id=level2_id,level2_name=level2_name,area_id=area_id,area_name=area_name,shipment_no=shipment_no,note=note,created_by=posted_by)

                                                    rptRowId = db.sm_rpt_transaction(insertRpt).id

                                                    # call update depot stock (type,cid,depotid,sl)
                                                    update_depot_stock('DELIVERY',c_id,req_depot,req_sl)

                                                    # distributor discount distribute
                                                    dist_discount_distribute_inv(inv_rowid)
                                                    
                                                    count+=1
                                                
                                    #----------    
                                    session.flash=str(count)+' Vouchers Posted Successfully.Shipment No:'+str(shipment_no)+'. '+str(errorStr)
                                    
                                    #---------------------
                                    autDelCronRows[0].update_record(auto_del_cron_flag=0)
                                    db.commit()
                                    #--------------
        else:
            session.flash='Invalid action'
            
    redirect('print_invoice')
    
    return ''

def dist_discount_distribute_inv(inv_rowid):
    inv_rowid=str(inv_rowid)

    invHeadRows = "select id,cid,depot_id,sl,actual_total_tp,dist_discount from sm_invoice_head where id='"+inv_rowid+"';"
    invHeadRows = db.executesql(invHeadRows, as_dict=True)

    for i in range(len(invHeadRows)):
        invHeadRowsS = invHeadRows[i]

        row_id = invHeadRowsS['id']
        c_id = invHeadRowsS['cid']
        req_depot = invHeadRowsS['depot_id']
        req_sl = invHeadRowsS['sl']
        actual_total_tp = invHeadRowsS['actual_total_tp']
        dist_discount = invHeadRowsS['dist_discount']

        invRows = db((db.sm_invoice.cid == c_id) & (db.sm_invoice.depot_id == req_depot) & (db.sm_invoice.sl == req_sl) & (db.sm_invoice.status == 'Invoiced') & (db.sm_invoice.quantity > 0)).select(db.sm_invoice.id, db.sm_invoice.actual_tp, db.sm_invoice.quantity)

        for row in invRows:
            actual_tp = float(row.actual_tp)
            quantity = int(row.quantity)

            total_tp=float(actual_tp*quantity)

            dist_discount_item=round((float(dist_discount)/float(actual_total_tp))*float(total_tp),6)

            row.update_record(dist_discount_item=dist_discount_item)

    return 'Done'

#========================= Show Invoice
def invoice_list_preview():
    c_id=session.cid
    
    if session.user_type=='Depot':
        req_depot=session.depot_id
    else:
        req_depot=request.vars.depotId
        user_depot_address=''
        depotRows = db((db.sm_depot.cid == session.cid) & (db.sm_depot.depot_id == req_depot)).select(db.sm_depot.field1, limitby=(0, 1))
        if depotRows:
            user_depot_address=depotRows[0].field1            
        session.user_depot_address = user_depot_address
    
    #--------------- Title
    response.title='Preview Invoice'
    
    #-------------
    vslList=[]
    vslListStr=request.vars.vslList
    
    if vslListStr==None:
        session.flash='need select voucher'
        redirect('print_invoice')
    else:
        pass
        
    vslListStr=urllib2.unquote(vslListStr)
    vslList=vslListStr.split(',')
    #-----------
    data_List=[]
    slList=[]
    for i in range(len(vslList)):
        req_sl=str(vslList[i]).strip()        
        if req_sl=='0':            
            continue
            
        slList.append(req_sl)
        
        #----------- 
        depot_id=''
        depot_name=''
        store_id=''
        store_name=''
        sl=0
        order_sl=0
        order_datetime=''
        delivery_date=''
        client_id=''
        client_name=''
        rep_id=''
        rep_name=''
        area_id=''
        area_name=''
        payment_mode=''
        discount=0
        note=''
        status=''
        level0_id=''
        level0_name=''
        discount_precent=0
        collection_amount=0
        collection_amount=0
        regular_disc_tp=0
        
        hRecords=db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==req_depot) & (db.sm_invoice_head.sl==req_sl)).select(db.sm_invoice_head.ALL,limitby=(0,1))
        if hRecords:        
            depot_id=hRecords[0].depot_id
            depot_name=hRecords[0].depot_name            
            sl=hRecords[0].sl
            store_id=hRecords[0].store_id
            store_name=hRecords[0].store_name            
            order_sl=hRecords[0].order_sl
            order_datetime=hRecords[0].order_datetime
            delivery_date=hRecords[0].delivery_date
            invoice_date=hRecords[0].invoice_date            
            client_id=hRecords[0].client_id
            client_name=hRecords[0].client_name
            rep_id=hRecords[0].rep_id
            rep_name=hRecords[0].rep_name            
            d_man_id=hRecords[0].d_man_id
            d_man_name=hRecords[0].d_man_name            
            area_id=hRecords[0].area_id
            area_name=hRecords[0].area_name            
            payment_mode=hRecords[0].payment_mode
            credit_note=hRecords[0].credit_note            
            discount=hRecords[0].discount                     
            note=hRecords[0].note
            status=hRecords[0].status            
            updated_by=hRecords[0].updated_by
            level0_id=hRecords[0].level0_id
            level0_name=hRecords[0].level0_name
            level1_id = hRecords[0].level1_id
            level1_name = hRecords[0].level1_name
            level2_id = hRecords[0].level2_id
            level2_name = hRecords[0].level2_name
            discount_precent=hRecords[0].discount_precent            
            collection_amount=hRecords[0].collection_amount
            regular_disc_tp=hRecords[0].regular_disc_tp
            posted_by = hRecords[0].posted_by
            return_tp = hRecords[0].return_tp
            return_vat = hRecords[0].return_vat
            return_discount = hRecords[0].return_discount
            return_sp_discount = hRecords[0].return_sp_discount
            
            address=''
            client_category=''
            owner_name=''
            contact_no1=''
            district=''
            client_old_id=''
            sub_category_name=''
            market_id=''
            market_name=''
            
            clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.client_id==client_id)).select(db.sm_client.ALL,limitby=(0,1))
            if clientRow:
                address=clientRow[0].address
                client_category=clientRow[0].category_id
                owner_name=clientRow[0].owner_name
                contact_no1=clientRow[0].contact_no1
                district=clientRow[0].district
                client_old_id=clientRow[0].client_old_id
                sub_category_name=clientRow[0].sub_category_name
                market_id=clientRow[0].market_id
                market_name=clientRow[0].market_name
            #--------------------
            p_sl=0
            vdDictList=[]
            
            records=db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==req_depot) & (db.sm_invoice.sl==req_sl)).select(db.sm_invoice.ALL,orderby=db.sm_invoice.item_name)
            for vdRow in records:        
                item_id=vdRow.item_id
                item_name=vdRow.item_name
                batch_id=vdRow.batch_id
                category_id=vdRow.category_id
                actual_tp=vdRow.actual_tp
                actual_vat=vdRow.actual_vat
                quantity=vdRow.quantity
                bonus_qty=vdRow.bonus_qty
                price=vdRow.price
                item_vat=vdRow.item_vat    
                short_note=vdRow.short_note
                item_unit=vdRow.item_unit
                
                promotion_type=vdRow.promotion_type
                bonus_applied_on_qty=vdRow.bonus_applied_on_qty
                discount_type=vdRow.discount_type
                item_discount=vdRow.item_discount
                item_discount_percent=vdRow.item_discount_percent
                discount_type_quantity=vdRow.discount_type_quantity
                
                p_sl+=1
                #------------------------
                vdDict= {'p_sl': p_sl,'item_id': item_id,'item_name': item_name,'batch_id':batch_id,'item_unit':item_unit,'category_id':category_id,'actual_tp':actual_tp,'actual_vat':actual_vat,'quantity': quantity,'bonus_qty':bonus_qty,'price': price,'item_vat': item_vat,'short_note': short_note,'promotion_type':promotion_type,'bonus_applied_on_qty':bonus_applied_on_qty,'discount_type':discount_type,'item_discount':item_discount,'item_discount_percent':item_discount_percent,'discount_type_quantity':discount_type_quantity}
                vdDictList.append(vdDict)
                
            vhDict={'depot_id':depot_id,'depot_name':depot_name,'sl':sl,'store_id':store_id,'store_name':store_name,'order_sl':order_sl,'order_datetime':order_datetime,'delivery_date':delivery_date,'invoice_date':invoice_date,'client_id':client_id,'client_old_id':client_old_id,'client_name':client_name,'client_category':client_category,'sub_category_name':sub_category_name,'market_id':market_id,'market_name':market_name,
                    'contact_no1':contact_no1,'owner_name':owner_name,'address':address,'district':district,'level0':level0_id,'level0_name':level0_name,'level1':level1_id,'level1_name':level1_name,'level2':level2_id,'level2_name':level2_name,'rep_id':rep_id,'rep_name':rep_name,'d_man_id':d_man_id,'d_man_name':d_man_name,'area_id':area_id,'area_name':area_name,'collection_amount':collection_amount,'status':status,'updated_by':updated_by,'regular_disc_tp':regular_disc_tp,'discount':discount,'discount_precent':discount_precent,'note':note,'payment_mode':payment_mode,'credit_note':credit_note,'return_tp':return_tp,'return_vat':return_vat,'return_discount':return_discount,'return_sp_discount':return_sp_discount,'vdList':vdDictList}
            data_List.append(vhDict)
            
    #------------------- print status (field2) update
    if len(slList)>0:
        db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==req_depot) & (db.sm_invoice_head.sl.belongs(slList))).update(field2=1)      

    # distribtor name
    dist_name=''
    distRows = db((db.sm_depot_distributor.cid == session.cid) & (db.sm_depot_distributor.depot_id == req_depot)).select(db.sm_depot_distributor.dist_name,limitby=(0, 1))
    if distRows:
        dist_name = distRows[0].dist_name

        #-------------------------
    return dict(data_List=data_List,dist_name=dist_name)



#=========================  Invoice Pending
def invoice_list_pending():
    c_id=session.cid
    
    if session.user_type=='Depot':
        req_depot=session.depot_id
    else:
        session.flash='Invalid Request'
        redirect('print_synopsis')
    
    #--------------- Title
    response.title='STP Pending'
    
    #-------------
    vslList=[]
    vslListStr=request.vars.vslList
    
    if vslListStr==None:
        session.flash='need select voucher'
        redirect('print_synopsis')
    else:
        pass
        
    vslListStr=urllib2.unquote(vslListStr)
    vslList=vslListStr.split(',')
    #-----------
    data_List=[]
    slList=[]
    for i in range(len(vslList)):
        req_sl=str(vslList[i]).strip()        
        if req_sl=='0':            
            continue
            
        slList.append(req_sl)
        
    #------------------- print status (field2) update
    if len(slList)>0:
        updateRows=db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==req_depot) & (db.sm_invoice_head.sl.belongs(slList)) & (db.sm_invoice_head.payment_mode=='CASH')& (db.sm_invoice_head.collection_amount<=0)).update(inv_pending_flag=1)
        if updateRows:
            session.flash='STP Pending Successfully'
        else:
            session.flash='Required Invoice of CASH and No collection'
    else:
        session.flash='Required select invoice'
    
    redirect('print_synopsis')
    

#=========================  Invoice Pending
def invoice_list_pending_free():
    c_id=session.cid
    
    if session.user_type=='Depot':
        req_depot=session.depot_id
    else:
        session.flash='Invalid Request'
        redirect('print_synopsis')
    
    #--------------- Title
    response.title='Cancel STP Pending'
    
    #-------------
    vslList=[]
    vslListStr=request.vars.vslList
    
    if vslListStr==None:
        session.flash='need select voucher'
        redirect('print_synopsis')
    else:
        pass
        
    vslListStr=urllib2.unquote(vslListStr)
    vslList=vslListStr.split(',')
    #-----------
    data_List=[]
    slList=[]
    for i in range(len(vslList)):
        req_sl=str(vslList[i]).strip()        
        if req_sl=='0':            
            continue
            
        slList.append(req_sl)
    
    #------------------- print status (field2) update
    if len(slList)>0:
        updateRows=db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==req_depot) & (db.sm_invoice_head.sl.belongs(slList)) & (db.sm_invoice_head.payment_mode=='CASH')& (db.sm_invoice_head.inv_pending_flag==1)).update(inv_pending_flag=0)
        if updateRows:
            session.flash='Cancel STP Pending Successfully'
        else:
            session.flash='Pending Invoice not available'
    else:
        session.flash='Required select invoice'
    
    redirect('print_synopsis')
    
#========================= Preview List
def preview_list():
    c_id=session.cid
    
    if session.user_type=='Depot':
        req_depot=session.depot_id
    else:
        req_depot=request.vars.depotId
        user_depot_address=''
        depotRows = db((db.sm_depot.cid == session.cid) & (db.sm_depot.depot_id == req_depot)).select(db.sm_depot.field1, limitby=(0, 1))
        if depotRows:
            user_depot_address=depotRows[0].field1            
        session.user_depot_address = user_depot_address
    
    #--------------- Title
    response.title='Preview List'
    
    #-------------
    #-----------
    invoice_dateFrom=''
    invoice_dateTo=''
    
    territory_id=''
    territory_name=''    
    
    d_man_id=''
    d_man_name=''
    
    search_from_sl=''
    search_to_sl=''
    paymentMode=''
    creditType=''
    #----------------------
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.sl!=0)
    qset=qset(db.sm_invoice_head.depot_id==req_depot)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    
    #----------
    if (session.btn_filter_printm_s):
        if session.search_dt_from!='' and session.search_dt_to!='':
            qset=qset((db.sm_invoice_head.invoice_date>=session.search_dt_from)&(db.sm_invoice_head.invoice_date<=session.search_dt_to))
            invoice_dateFrom=session.search_dt_from
            invoice_dateTo=session.search_dt_to
            
        if session.search_from_sl>0 and session.search_to_sl>0:
            qset=qset((db.sm_invoice_head.sl>=session.search_from_sl)&(db.sm_invoice_head.sl<=session.search_to_sl))
            search_from_sl=session.search_from_sl
            search_to_sl=session.search_to_sl
            
        #------------
        if (session.search_type_printm_s=='REPID'):                
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.rep_id==searchValue)
            
        elif (session.search_type_printm_s=='ROUTEID'):
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.area_id==searchValue)
            
            territory_id=searchValue
            if territory_id!='':
                areaRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id) & (db.sm_level.is_leaf == '1')).select(db.sm_level.level_name,db.sm_level.level0,db.sm_level.level0_name,limitby=(0,1))
                if areaRow:
                    territory_name=areaRow[0].level_name
                    
        elif (session.search_type_printm_s=='CLIENTID'):
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.client_id==searchValue)
        
        elif (session.search_type_printm_s=='SHIPMENT'):
            searchValue=str(session.search_value_printm_s).strip()
            qset=qset(db.sm_invoice_head.shipment_no==searchValue)
        
        #----------
        if session.print_status=='Pending':
            qset=qset(db.sm_invoice_head.field2==0)
            
        #----------
        if session.paymentMode!='':
            qset=qset(db.sm_invoice_head.payment_mode==session.paymentMode)
            paymentMode=session.paymentMode
            
        #----------
        if session.creditType!='':
            qset=qset(db.sm_invoice_head.credit_note==session.creditType)
            creditType=session.creditType
            
        #----------
        if not(session.d_man_id_report=='' or session.d_man_id_report==None):
            searchValue=str(session.d_man_id_report).split('|')[0]
            qset=qset(db.sm_invoice_head.d_man_id==searchValue)
            
            d_man_id=searchValue
            dmanRecords=db((db.sm_delivery_man.cid==c_id)& (db.sm_delivery_man.depot_id==req_depot) & (db.sm_delivery_man.d_man_id==d_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
            if dmanRecords:
                d_man_name=dmanRecords[0].name
    
    hRecords=qset.select(db.sm_invoice_head.ALL,orderby=db.sm_invoice_head.level2_id|db.sm_invoice_head.rep_id|db.sm_invoice_head.area_id)
    
    data_List=[]
    for hRec in hRecords:      
          
        depot_id=hRec.depot_id
        depot_name=hRec.depot_name            
        sl=hRec.sl
        store_id=hRec.store_id
        store_name=hRec.store_name            
        order_sl=hRec.order_sl
        order_datetime=hRec.order_datetime
        delivery_date=hRec.delivery_date
        invoice_date=hRec.invoice_date            
        client_id=hRec.client_id
        client_name=hRec.client_name
        rep_id=hRec.rep_id
        rep_name=hRec.rep_name            
        #d_man_id=hRec.d_man_id
        #d_man_name=hRec.d_man_name            
        area_id=hRec.area_id
        area_name=hRec.area_name            
        payment_mode=hRec.payment_mode    
        discount=hRec.discount                     
        note=hRec.note
        status=hRec.status            
        updated_by=hRec.updated_by
        level0_id=hRec.level0_id
        level0_name=hRec.level0_name
        level2_id=hRec.level2_id
        level2_name=hRec.level2_name
        discount_precent=hRec.discount_precent
        
        address=''
        client_category=''
        owner_name=''
        contact_no1=''
        district=''
        client_old_id=''
        sub_category_name=''
        market_id=''
        market_name=''
        
        clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.client_id==client_id)).select(db.sm_client.ALL,limitby=(0,1))
        if clientRow:
            address=clientRow[0].address
            client_category=clientRow[0].category_id
            owner_name=clientRow[0].owner_name
            contact_no1=clientRow[0].contact_no1
            district=clientRow[0].district
            client_old_id=clientRow[0].client_old_id
            sub_category_name=clientRow[0].sub_category_name
            market_id=clientRow[0].market_id
            market_name=clientRow[0].market_name
        #--------------------
        
        vhDict={'depot_id':depot_id,'depot_name':depot_name,'sl':sl,'store_id':store_id,'store_name':store_name,'order_sl':order_sl,'order_datetime':order_datetime,'delivery_date':delivery_date,'invoice_date':invoice_date,'client_id':client_id,'client_old_id':client_old_id,'client_name':client_name,'client_category':client_category,'sub_category_name':sub_category_name,'market_id':market_id,'market_name':market_name,
                'contact_no1':contact_no1,'owner_name':owner_name,'address':address,'district':district,'level0':level0_id,'level0_name':level0_name,'level2_id':level2_id,'level2_name':level2_name,'rep_id':rep_id,'rep_name':rep_name,'d_man_id':d_man_id,'d_man_name':d_man_name,'area_id':area_id,'area_name':area_name,'status':status,'updated_by':updated_by,'discount':discount,'discount_precent':discount_precent,'note':note,'payment_mode':payment_mode}
        
        data_List.append(vhDict)
    
    #data_List=data_List.sort(key=itemgetter('sl'), reverse=False)
    
    #-------------------------
    return dict(data_List=data_List,depot_id=depot_id,depot_name=depot_name,territory_id=territory_id,territory_name=territory_name,invoice_dateFrom=invoice_dateFrom,invoice_dateTo=invoice_dateTo,d_man_id=d_man_id,d_man_name=d_man_name,search_from_sl=search_from_sl,search_to_sl=search_to_sl,paymentMode=paymentMode,creditType=creditType)
    
#========================= Preview List
def preview_list_selected():
    c_id=session.cid
    
    if session.user_type=='Depot':
        req_depot=session.depot_id
    else:
        req_depot=request.vars.depotId
        user_depot_address=''
        depotRows = db((db.sm_depot.cid == session.cid) & (db.sm_depot.depot_id == req_depot)).select(db.sm_depot.field1, limitby=(0, 1))
        if depotRows:
            user_depot_address=depotRows[0].field1            
        session.user_depot_address = user_depot_address
    
    #--------------- Title
    response.title='Preview List'
    
    #-------------
    vslList=[]
    vslListStr=request.vars.vslList
    
    if vslListStr==None:
        session.flash='need select voucher'
        redirect('print_invoice')
    else:
        pass
        
    vslListStr=urllib2.unquote(vslListStr)
    vslList=vslListStr.split(',')
        
    #-----------
    data_List=[]
    slList=[]
    for i in range(len(vslList)):
        req_sl=str(vslList[i]).strip()        
        if req_sl=='0':            
            continue
            
        slList.append(req_sl)
        
        #----------- 
        depot_id=''
        depot_name=''
        store_id=''
        store_name=''
        sl=0
        order_sl=0
        order_datetime=''
        delivery_date=''
        client_id=''
        client_name=''
        rep_id=''
        rep_name=''
        area_id=''
        area_name=''
        payment_mode=''
        discount=0
        note=''
        status=''
        level0_id=''
        level0_name=''
        discount_precent=0
        
        hRecords=db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==req_depot) & (db.sm_invoice_head.sl==req_sl)).select(db.sm_invoice_head.ALL,limitby=(0,1))
        if hRecords:        
            depot_id=hRecords[0].depot_id
            depot_name=hRecords[0].depot_name            
            sl=hRecords[0].sl
            store_id=hRecords[0].store_id
            store_name=hRecords[0].store_name            
            order_sl=hRecords[0].order_sl
            order_datetime=hRecords[0].order_datetime
            delivery_date=hRecords[0].delivery_date
            invoice_date=hRecords[0].invoice_date            
            client_id=hRecords[0].client_id
            client_name=hRecords[0].client_name
            rep_id=hRecords[0].rep_id
            rep_name=hRecords[0].rep_name            
            d_man_id=hRecords[0].d_man_id
            d_man_name=hRecords[0].d_man_name            
            area_id=hRecords[0].area_id
            area_name=hRecords[0].area_name            
            payment_mode=hRecords[0].payment_mode    
            discount=hRecords[0].discount                     
            note=hRecords[0].note
            status=hRecords[0].status            
            updated_by=hRecords[0].updated_by
            level0_id=hRecords[0].level0_id
            level0_name=hRecords[0].level0_name
            discount_precent=hRecords[0].discount_precent
            
            address=''
            client_category=''
            owner_name=''
            contact_no1=''
            district=''
            client_old_id=''
            sub_category_name=''
            market_id=''
            market_name=''
            
            clientRow=db((db.sm_client.cid==c_id)&(db.sm_client.client_id==client_id)).select(db.sm_client.ALL,limitby=(0,1))
            if clientRow:
                address=clientRow[0].address
                client_category=clientRow[0].category_id
                owner_name=clientRow[0].owner_name
                contact_no1=clientRow[0].contact_no1
                district=clientRow[0].district
                client_old_id=clientRow[0].client_old_id
                sub_category_name=clientRow[0].sub_category_name
                market_id=clientRow[0].market_id
                market_name=clientRow[0].market_name
            #--------------------
#             p_sl=0
#             vdDictList=[]
#             
#             records=db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==req_depot) & (db.sm_invoice.sl==req_sl)).select(db.sm_invoice.ALL,orderby=db.sm_invoice.item_name)
#             for vdRow in records:        
#                 item_id=vdRow.item_id
#                 item_name=vdRow.item_name
#                 batch_id=vdRow.batch_id
#                 category_id=vdRow.category_id
#                 quantity=vdRow.quantity
#                 bonus_qty=vdRow.bonus_qty
#                 price=vdRow.price
#                 item_vat=vdRow.item_vat    
#                 short_note=vdRow.short_note
#                 
#                 p_sl+=1
#                 #------------------------
#                 vdDict= {'p_sl': p_sl,'item_id': item_id,'item_name': item_name,'batch_id':batch_id,'category_id':category_id,'quantity': quantity,'bonus_qty':bonus_qty,'price': price,'item_vat': item_vat,'short_note': short_note}
#                 vdDictList.append(vdDict)                
#             vhDict={'depot_id':depot_id,'depot_name':depot_name,'sl':sl,'store_id':store_id,'store_name':store_name,'order_sl':order_sl,'order_datetime':order_datetime,'delivery_date':delivery_date,'invoice_date':invoice_date,'client_id':client_id,'client_old_id':client_old_id,'client_name':client_name,'client_category':client_category,'sub_category_name':sub_category_name,'market_id':market_id,'market_name':market_name,
#                     'contact_no1':contact_no1,'owner_name':owner_name,'address':address,'district':district,'level0':level0_id,'level0_name':level0_name,'rep_id':rep_id,'rep_name':rep_name,'d_man_id':d_man_id,'d_man_name':d_man_name,'area_id':area_id,'area_name':area_name,'status':status,'updated_by':updated_by,'discount':discount,'discount_precent':discount_precent,'note':note,'payment_mode':payment_mode,'vdList':vdDictList}
            
            vhDict={'depot_id':depot_id,'depot_name':depot_name,'sl':sl,'store_id':store_id,'store_name':store_name,'order_sl':order_sl,'order_datetime':order_datetime,'delivery_date':delivery_date,'invoice_date':invoice_date,'client_id':client_id,'client_old_id':client_old_id,'client_name':client_name,'client_category':client_category,'sub_category_name':sub_category_name,'market_id':market_id,'market_name':market_name,
                    'contact_no1':contact_no1,'owner_name':owner_name,'address':address,'district':district,'level0':level0_id,'level0_name':level0_name,'rep_id':rep_id,'rep_name':rep_name,'d_man_id':d_man_id,'d_man_name':d_man_name,'area_id':area_id,'area_name':area_name,'status':status,'updated_by':updated_by,'discount':discount,'discount_precent':discount_precent,'note':note,'payment_mode':payment_mode}
            
            data_List.append(vhDict)
    
    #data_List=data_List.sort(key=itemgetter('sl'), reverse=False)
    
    #-------------------------
    return dict(data_List=data_List,depot_id=depot_id,depot_name=depot_name)
    
#======================= Print Synopsis List
def print_synopsis():
    c_id=session.cid
    
    #----------------
    response.title='Print-Synopsis'
    #Check access permission
    #----------Task assaign----------
    task_id='rm_print_manager_view'
    access_permission=check_role(task_id)
    if (access_permission==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
        
    #Set text for filter    
    btn_filter_printm_s=request.vars.btn_filter
    btn_all=request.vars.btn_all
    
    currentDate=current_date
    
    invoiceFlag=0
    pageBreakFlag=1
    
    search_type=str(request.vars.search_type).strip()
    search_value=str(request.vars.search_value).strip()
    search_dt_from=str(request.vars.from_dt).strip()
    search_dt_to=str(request.vars.to_dt).strip()
    print_status=str(request.vars.print_status).strip()
    paymentMode=str(request.vars.paymentMode).strip()
    creditType=str(request.vars.creditType).strip()
    search_from_sl=str(request.vars.search_from_sl).strip()
    search_to_sl=str(request.vars.search_to_sl).strip()
    d_man_id_report=str(request.vars.d_man_id_report).strip().upper()
    invPending=str(request.vars.invPending).strip()
    
    reqPage=len(request.args)
    # Set sessions for filter
    if btn_filter_printm_s:
        session.btn_filter_printm_s=btn_filter_printm_s        
        session.search_type_printm_s=search_type
        session.search_value_printm_s=search_value        
        session.print_status=print_status        
        session.paymentMode=paymentMode
        session.creditType=creditType
        session.d_man_id_report=d_man_id_report
        session.invPending=invPending
        # Check SL is integer or not        
        from_sl=0
        if not(search_from_sl=='' or search_from_sl==None):
            try:
                from_sl=int(search_from_sl)
                session.search_from_sl=from_sl
            except:
                session.search_from_sl=from_sl                
        else:
            session.search_from_sl=from_sl
        
        #-----------------
        to_sl=0
        if not(search_to_sl=='' or search_to_sl==None):
            try:
                to_sl=int(search_to_sl)
                session.search_to_sl=to_sl
            except:
                session.search_to_sl=to_sl                
        else:
            session.search_to_sl=to_sl
            
        #---
        try:
            currentDate=datetime.datetime.strptime(search_dt_from,'%Y-%m-%d').strftime('%Y-%m-%d')
            session.search_dt_from=currentDate
        except:
            session.search_dt_from=''
            
        #---
        try:
            currentDateTo=datetime.datetime.strptime(search_dt_to,'%Y-%m-%d').strftime('%Y-%m-%d')
            session.search_dt_to=currentDateTo
        except:
            session.search_dt_to=''
            
        reqPage=0
        
    elif btn_all:
        session.btn_filter_printm_s=None        
        session.search_type_printm_s=None
        session.search_value_printm_s=None
        session.search_dt_from=None   
        session.search_dt_to=None
        session.paymentMode=None
        session.creditType=None
        session.search_from_sl=None
        session.search_to_sl=None
        session.d_man_id_report=None        
        session.print_status=None
        session.invPending=None
        reqPage=0
        
    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging  
    
    
    # Set query based on search type
    deliveryManRows =''
    records=''
    totalRecords=0
    totalCount=0
    
    qsetHead=db()
    
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.sl!=0)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    
    if (session.user_type!='Depot'):
        records=''
        response.flash='Only depot user can print'
    else:        
        qset=qset(db.sm_invoice_head.depot_id==session.depot_id)
        
        #----------
        
        if (session.btn_filter_printm_s):
            if session.search_dt_from!='' and session.search_dt_to!='':
                qset=qset((db.sm_invoice_head.invoice_date>=session.search_dt_from)&(db.sm_invoice_head.invoice_date<=session.search_dt_to))
                
            if session.search_from_sl>0 and session.search_to_sl>0:
                qset=qset((db.sm_invoice_head.sl>=session.search_from_sl)&(db.sm_invoice_head.sl<=session.search_to_sl))
                
            #------------
            if (session.search_type_printm_s=='REPID'):                
                searchValue=str(session.search_value_printm_s).split('|')[0]
                qset=qset(db.sm_invoice_head.rep_id==searchValue)
            
            elif (session.search_type_printm_s=='ROUTEID'):
                searchValue=str(session.search_value_printm_s).split('|')[0]
                qset=qset(db.sm_invoice_head.area_id==searchValue)
            
            elif (session.search_type_printm_s=='CLIENTID'):
                searchValue=str(session.search_value_printm_s).split('|')[0]
                qset=qset(db.sm_invoice_head.client_id==searchValue)
            
            elif (session.search_type_printm_s=='SHIPMENT'):
                searchValue=str(session.search_value_printm_s).strip()
                qset=qset(db.sm_invoice_head.shipment_no==searchValue)
                
            #----------
            if session.print_status=='Pending':
                qset=qset(db.sm_invoice_head.field2==0)
                
            #----------
            if session.paymentMode!='':
                qset=qset(db.sm_invoice_head.payment_mode==session.paymentMode)
            
            #----------
            if session.creditType!='':
                qset=qset(db.sm_invoice_head.credit_note==session.creditType)
                
            #----------
            if session.invPending!='':
                qset=qset(db.sm_invoice_head.inv_pending_flag==session.invPending)
                
                
        #get dp list
        deliveryManRows = qset.select(db.sm_invoice_head.d_man_id,db.sm_invoice_head.d_man_name.max(), orderby=db.sm_invoice_head.d_man_name, groupby=db.sm_invoice_head.d_man_id)
        
        #----------
        if not(session.d_man_id_report=='' or session.d_man_id_report==None):
            searchValue=str(session.d_man_id_report).split('|')[0]
            qset=qset(db.sm_invoice_head.d_man_id==searchValue)
        
        records=qset.select(db.sm_invoice_head.ALL,orderby=~db.sm_invoice_head.sl,limitby=limitby)
        
        totalRecords=len(records)
    
    totalCount=qset.count()
    
    #return db._lastsql
    #------------ filter form
    filterform =SQLFORM(db.sm_search_date,
                  fields=['from_dt','to_dt']
                  )
    
    if (session.search_dt_from=='' or session.search_dt_from==None):
        filterform.vars.from_dt=''
    else:
        filterform.vars.from_dt=session.search_dt_from
    
    if (session.search_dt_to=='' or session.search_dt_to==None):
        filterform.vars.to_dt=''
    else:
        filterform.vars.to_dt=session.search_dt_to
    
    
    if filterform.accepts(request.vars,session):
        pass
        
    invoiceTermRows=db((db.sm_category_type.cid==session.cid) & (db.sm_category_type.type_name=='PAYMENT_MODE')).select(db.sm_category_type.cat_type_id,orderby=db.sm_category_type.cat_type_id)
    creditTypeRows=db((db.sm_category_type.cid==session.cid) & (db.sm_category_type.type_name=='CREDIT_NOTE')).select(db.sm_category_type.cat_type_id,orderby=db.sm_category_type.cat_type_id)
    
    return dict(records=records,filterform=filterform,currentDate=currentDate,totalRecords=totalRecords,totalCount=totalCount,invoiceTermRows=invoiceTermRows,creditTypeRows=creditTypeRows,invoiceFlag=invoiceFlag,pageBreakFlag=pageBreakFlag,deliveryManRows=deliveryManRows,page=page,items_per_page=items_per_page,access_permission=access_permission)
    
def invoice_reports():
#    vslList=[]
#    slListStr=request.vars.slStrListReport
#    if slListStr=='' or slListStr==None:
#        session.flash='Required selected confirmation'
#        redirect('print_invoice')
#    else:
#        pass
    
    btn_preview_list=request.vars.btn_preview_list
    btn_invoice_list=request.vars.btn_invoice_list
    btn_invoice_item=request.vars.btn_invoice_item
    btn_synopsis_inv_item_beforeDel=request.vars.btn_synopsis_inv_item_beforeDel
    btn_synopsis_inv_item_beforeDel_withoutbatch=request.vars.btn_synopsis_inv_item_beforeDel_withoutbatch
    
    btn_invoice_item_sd_afterDel=request.vars.btn_invoice_item_sd_afterDel
    btn_invoice_item_ad_afterDel=request.vars.btn_invoice_item_ad_afterDel
    btn_invoice_item_ad_afterDel_retDet=request.vars.btn_invoice_item_ad_afterDel_retDet
    
    btn_synopsis_sd_ad_afterDel=request.vars.btn_synopsis_sd_ad_afterDel
    btn_synopsis_sd_ad_afterDel_withoutbatch=request.vars.btn_synopsis_sd_ad_afterDel_withoutbatch
    btn_synopsis_sd_ad_afterDel_withoutbatch_retDet=request.vars.btn_synopsis_sd_ad_afterDel_withoutbatch_retDet
    
    
    if btn_invoice_list:
        redirect(URL('invoice_list_synopsis'))
        
    elif btn_invoice_item:
        redirect(URL('invoice_item_list_synopsis'))
    
    elif btn_synopsis_inv_item_beforeDel:
        redirect(URL('invoice_synopsis_before_del'))
    
    elif btn_synopsis_inv_item_beforeDel_withoutbatch:
        redirect(URL('invoice_synopsis_before_del_withoutbatch'))
    
    elif btn_invoice_item_sd_afterDel:
        redirect(URL('invoice_item_list_synopsis_sd_after_del'))
        
    elif btn_invoice_item_ad_afterDel:
        redirect(URL('invoice_item_list_synopsis_ad_after_del'))
    
    elif btn_invoice_item_ad_afterDel_retDet:
        redirect(URL('invoice_item_list_synopsis_ad_after_del_retDet'))
    
    elif btn_synopsis_sd_ad_afterDel:
        redirect(URL('invoice_synopsis_sd_ad_after_del'))
    
    elif btn_synopsis_sd_ad_afterDel_withoutbatch:
        redirect(URL('invoice_synopsis_sd_ad_after_del_withoutbatch'))
        
    elif btn_synopsis_sd_ad_afterDel_withoutbatch_retDet:
        redirect(URL('invoice_synopsis_sd_ad_after_del_withoutbatch_retDet'))
        
    elif btn_preview_list:
        redirect(URL('preview_list'))
        
    redirect('print_invoice')

#========================= Show Invoice invoice_list_synopsis
def invoice_list_synopsis():
    c_id=session.cid
    req_depot=session.depot_id
    
    #--------------- Title
    response.title='Synopsis-Invoice List'
    #-------------
    
    #-----------
    invoice_dateFrom=''
    invoice_dateTo=''
    
    territory_id=''
    territory_name=''    
    
    d_man_id=''
    d_man_name=''
    paymentMode=''
    search_from_sl=''
    search_to_sl=''
    creditType=''
    #----------------------
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.sl!=0)
    qset=qset(db.sm_invoice_head.depot_id==req_depot)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    
    #----------
    if (session.btn_filter_printm_s):
        if session.search_dt_from!='' and session.search_dt_to!='':
            qset=qset((db.sm_invoice_head.invoice_date>=session.search_dt_from)&(db.sm_invoice_head.invoice_date<=session.search_dt_to))
            invoice_dateFrom=session.search_dt_from
            invoice_dateTo=session.search_dt_to
            
        if session.search_from_sl>0 and session.search_to_sl>0:
            qset=qset((db.sm_invoice_head.sl>=session.search_from_sl)&(db.sm_invoice_head.sl<=session.search_to_sl))
            search_from_sl=session.search_from_sl
            search_to_sl=session.search_to_sl
            
        #------------
        if (session.search_type_printm_s=='REPID'):                
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.rep_id==searchValue)
            
        elif (session.search_type_printm_s=='ROUTEID'):
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.area_id==searchValue)
            
            territory_id=searchValue
            if territory_id!='':
                areaRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id) & (db.sm_level.is_leaf == '1')).select(db.sm_level.level_name,db.sm_level.level0,db.sm_level.level0_name,limitby=(0,1))
                if areaRow:
                    territory_name=areaRow[0].level_name
                    
        elif (session.search_type_printm_s=='CLIENTID'):
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.client_id==searchValue)
        
        elif (session.search_type_printm_s=='SHIPMENT'):
            searchValue=str(session.search_value_printm_s).strip()
            qset=qset(db.sm_invoice_head.shipment_no==searchValue)
            
        #----------
        if session.print_status=='Pending':
            qset=qset(db.sm_invoice_head.field2==0)
            
        #----------
        if session.paymentMode!='':
            qset=qset(db.sm_invoice_head.payment_mode==session.paymentMode)
            paymentMode=session.paymentMode
            
        #----------
        if session.creditType!='':
            qset=qset(db.sm_invoice_head.credit_note==session.creditType)
            creditType=session.creditType
            
        #----------
        if not(session.d_man_id_report=='' or session.d_man_id_report==None):
            searchValue=str(session.d_man_id_report).split('|')[0]
            qset=qset(db.sm_invoice_head.d_man_id==searchValue)
            
            d_man_id=searchValue
            dmanRecords=db((db.sm_delivery_man.cid==c_id)& (db.sm_delivery_man.depot_id==req_depot) & (db.sm_delivery_man.d_man_id==d_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
            if dmanRecords:
                d_man_name=dmanRecords[0].name
                
    records=qset.select(db.sm_invoice_head.ALL,orderby=db.sm_invoice_head.sl)
    
    #---------------------- maximum market Name
    maxMarketID=''
    maxmarketName=''
    maxCount=0
    headRecords2=qset.select(db.sm_invoice_head.market_id,db.sm_invoice_head.market_name.max(),db.sm_invoice_head.id.count(),groupby=db.sm_invoice_head.market_id)
    for headRec2 in headRecords2:
        market_id=headRec2.sm_invoice_head.market_id
        market_name=headRec2[db.sm_invoice_head.market_name.max()]
        market_count=headRec2[db.sm_invoice_head.id.count()]        
        if market_count>maxCount:
            maxMarketID=market_id
            maxmarketName=market_name
            maxCount=market_count
        else:
            continue
    
    #-------------------------
    return dict(records=records,maxMarketID=maxMarketID,maxmarketName=maxmarketName,paymentMode=paymentMode,search_from_sl=search_from_sl,search_to_sl=search_to_sl,territory_id=territory_id,territory_name=territory_name,invoice_dateFrom=invoice_dateFrom,invoice_dateTo=invoice_dateTo,d_man_id=d_man_id,d_man_name=d_man_name,creditType=creditType)


#========================= Show Invoice invoice_list_synopsis
def invoice_list_synopsis_download():
    c_id=session.cid
    req_depot=session.depot_id
    
    #--------------- Title
    response.title='Download-Synopsis-Invoice List'
    #-------------
    
    #-----------
    invoice_dateFrom=''
    invoice_dateTo=''
    
    territory_id=''
    territory_name=''    
    
    d_man_id=''
    d_man_name=''
    paymentMode=''
    search_from_sl=''
    search_to_sl=''
    creditType=''
    #----------------------
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.sl!=0)
    qset=qset(db.sm_invoice_head.depot_id==req_depot)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    
    #----------
    if (session.btn_filter_printm_s):
        if session.search_dt_from!='' and session.search_dt_to!='':
            qset=qset((db.sm_invoice_head.invoice_date>=session.search_dt_from)&(db.sm_invoice_head.invoice_date<=session.search_dt_to))
            invoice_dateFrom=session.search_dt_from
            invoice_dateTo=session.search_dt_to
            
        if session.search_from_sl>0 and session.search_to_sl>0:
            qset=qset((db.sm_invoice_head.sl>=session.search_from_sl)&(db.sm_invoice_head.sl<=session.search_to_sl))
            search_from_sl=session.search_from_sl
            search_to_sl=session.search_to_sl
            
        #------------
        if (session.search_type_printm_s=='REPID'):                
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.rep_id==searchValue)
            
        elif (session.search_type_printm_s=='ROUTEID'):
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.area_id==searchValue)
            
            territory_id=searchValue
            if territory_id!='':
                areaRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id) & (db.sm_level.is_leaf == '1')).select(db.sm_level.level_name,db.sm_level.level0,db.sm_level.level0_name,limitby=(0,1))
                if areaRow:
                    territory_name=areaRow[0].level_name
                    
        elif (session.search_type_printm_s=='CLIENTID'):
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.client_id==searchValue)
        
        elif (session.search_type_printm_s=='SHIPMENT'):
            searchValue=str(session.search_value_printm_s).strip()
            qset=qset(db.sm_invoice_head.shipment_no==searchValue)
            
        #----------
        if session.print_status=='Pending':
            qset=qset(db.sm_invoice_head.field2==0)
            
        #----------
        if session.paymentMode!='':
            qset=qset(db.sm_invoice_head.payment_mode==session.paymentMode)
            paymentMode=session.paymentMode
            
        #----------
        if session.creditType!='':
            qset=qset(db.sm_invoice_head.credit_note==session.creditType)
            creditType=session.creditType
            
        #----------
        if not(session.d_man_id_report=='' or session.d_man_id_report==None):
            searchValue=str(session.d_man_id_report).split('|')[0]
            qset=qset(db.sm_invoice_head.d_man_id==searchValue)
            
            d_man_id=searchValue
            dmanRecords=db((db.sm_delivery_man.cid==c_id)& (db.sm_delivery_man.depot_id==req_depot) & (db.sm_delivery_man.d_man_id==d_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
            if dmanRecords:
                d_man_name=dmanRecords[0].name
                
    records=qset.select(db.sm_invoice_head.ALL,orderby=db.sm_invoice_head.sl)
    
    #---------------------- maximum market Name
    maxMarketID=''
    maxmarketName=''
    maxCount=0
    headRecords2=qset.select(db.sm_invoice_head.market_id,db.sm_invoice_head.market_name.max(),db.sm_invoice_head.id.count(),groupby=db.sm_invoice_head.market_id)
    for headRec2 in headRecords2:
        market_id=headRec2.sm_invoice_head.market_id
        market_name=headRec2[db.sm_invoice_head.market_name.max()]
        market_count=headRec2[db.sm_invoice_head.id.count()]        
        if market_count>maxCount:
            maxMarketID=market_id
            maxmarketName=market_name
            maxCount=market_count
        else:
            continue
    
    
    #-------------------------    
    if paymentMode=='':
        termsStr='ALL'
    else:
        termsStr=paymentMode
        
        if paymentMode=='CREDIT':
            if creditType=='':
                termsStr+='(ALL)'
            else:
                termsStr+='('+creditType+')'
    
    myString='SYNOPSIS (Invoice List)-Before Delivery:,'+str(territory_id)+'\n'
    myString+='Market:,'+str(maxMarketID)+'|'+str(maxmarketName)+'\n'
    myString+='Delivery Person ID:,'+str(d_man_id)+'\n'
    myString+='Delivery Person Name:'+','+str(d_man_name)+'\n'
    myString+='Sales Term:,'+str(termsStr)+'\n'
    myString+='From Invoice:,'+str(search_from_sl)+'\n'
    myString+='To Invoice Range:'+','+str(search_to_sl)+'\n'
    myString+='From Date:,'+str(invoice_dateFrom)+'\n'
    myString+='To Date:,'+str(invoice_dateTo)+'\n'
    
    if territory_id!='':
        myString+=str(territory_id)+' Territory wise'+'\n'
    elif d_man_id!='':
        myString+='DP wise'+'\n'
    
    
    invoice_total_tp=0.0
    vat_total=0.0
    discount_total=0.0
    totalSpAmt=0.0
    netInvAmt_total=0.0    
    netTotalOS=0.0
    totalOs=0
    
    rowSl=0
    myString+='Sl.No,Invoice No,Invoice Date,Cust.ID,Customer Name,TP,VAT,Disc,Sp.Disc,Invocie Net,Previous O/S,Total O/S,Credit Limit'+'\n'
    for record in records:
        rowSl+=1        
        invNo=str(session.prefix_invoice)+'INV'+str(record.depot_id)+'-'+str(record.sl)                                                           
        invoice_date=record.invoice_date
        client_id=record.client_id
        client_name=str(record.client_name).replace(',', ' ')        
        invTpAmt=round(record.actual_total_tp,2)
        invoice_total_tp+=invTpAmt
        vatAmt=round(record.vat_total_amount,2)
        vat_total+=vatAmt
        discountAmt=round(record.discount,2)
        discount_total+=discountAmt
        spAmt=round(record.sp_discount,2)
        totalSpAmt+=spAmt
        netInvAmt=round(invTpAmt+vatAmt-(discountAmt+spAmt),2)
        netInvAmt_total+=netInvAmt
        
        osAmt=round(record.previous_ost_amt,2)
        totalOs+=osAmt
        
        netOstAmt=round(netInvAmt+osAmt,2)
        netTotalOS+=netOstAmt
        
        client_limit_amt=record.client_limit_amt
        
        #------------------------        
        myString+=str(rowSl)+','+str(invNo)+','+str(invoice_date)+','+str(client_id)+','+str(client_name)+','+str(invTpAmt)+','+str(vatAmt)+','+str(discountAmt)+','+str(spAmt)+','+str(netInvAmt)+','+str(osAmt)+','+str(netOstAmt)+','+str(client_limit_amt)+'\n'
    
    myString+='Total:,,,,,'+str(invoice_total_tp)+','+str(vat_total)+','+str(discount_total)+','+str(totalSpAmt)+','+str(netInvAmt_total)+','+str(totalOs)+','+str(netTotalOS)+'\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_synopsisInvoiceListBeforeDelivery.csv'   
    return str(myString)


#========================= Show Invoice invoice_list_synopsis
def invoice_synopsis_before_del():
    c_id=session.cid
    req_depot=session.depot_id
    
    #--------------- Title
    response.title='5.3A Synopsis-Item List+Invoice Before delivery'
    #-------------
    
    #-----------
    invoice_dateFrom=''
    invoice_dateTo=''
    
    territory_id=''
    territory_name=''    
    
    d_man_id=''
    d_man_name=''
    paymentMode=''
    search_from_sl=''
    search_to_sl=''
    creditType=''
    #----------------------
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.sl!=0)
    qset=qset(db.sm_invoice_head.depot_id==req_depot)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    
    #----------
    if (session.btn_filter_printm_s):
        if session.search_dt_from!='' and session.search_dt_to!='':
            qset=qset((db.sm_invoice_head.invoice_date>=session.search_dt_from)&(db.sm_invoice_head.invoice_date<=session.search_dt_to))
            invoice_dateFrom=session.search_dt_from
            invoice_dateTo=session.search_dt_to
            
        if session.search_from_sl>0 and session.search_to_sl>0:
            qset=qset((db.sm_invoice_head.sl>=session.search_from_sl)&(db.sm_invoice_head.sl<=session.search_to_sl))
            search_from_sl=session.search_from_sl
            search_to_sl=session.search_to_sl
            
        #------------
        if (session.search_type_printm_s=='REPID'):                
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.rep_id==searchValue)
            
        elif (session.search_type_printm_s=='ROUTEID'):
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.area_id==searchValue)
            
            territory_id=searchValue
            if territory_id!='':
                areaRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id) & (db.sm_level.is_leaf == '1')).select(db.sm_level.level_name,db.sm_level.level0,db.sm_level.level0_name,limitby=(0,1))
                if areaRow:
                    territory_name=areaRow[0].level_name
                    
        elif (session.search_type_printm_s=='CLIENTID'):
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.client_id==searchValue)
        
        elif (session.search_type_printm_s=='SHIPMENT'):
            searchValue=str(session.search_value_printm_s).strip()
            qset=qset(db.sm_invoice_head.shipment_no==searchValue)
            
        #----------
        if session.print_status=='Pending':
            qset=qset(db.sm_invoice_head.field2==0)
            
        #----------
        if session.paymentMode!='':
            qset=qset(db.sm_invoice_head.payment_mode==session.paymentMode)
            paymentMode=session.paymentMode
            
        #----------
        if session.creditType!='':
            qset=qset(db.sm_invoice_head.credit_note==session.creditType)
            creditType=session.creditType
            
        #----------
        if not(session.d_man_id_report=='' or session.d_man_id_report==None):
            searchValue=str(session.d_man_id_report).split('|')[0]
            qset=qset(db.sm_invoice_head.d_man_id==searchValue)
            
            d_man_id=searchValue
            dmanRecords=db((db.sm_delivery_man.cid==c_id)& (db.sm_delivery_man.depot_id==req_depot) & (db.sm_delivery_man.d_man_id==d_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
            if dmanRecords:
                d_man_name=dmanRecords[0].name
                
    records=qset.select(db.sm_invoice_head.ALL,orderby=db.sm_invoice_head.sl)
    
    #---------------------- maximum market Name
    maxMarketID=''
    maxmarketName=''
    maxCount=0
    headRecords2=qset.select(db.sm_invoice_head.market_id,db.sm_invoice_head.market_name.max(),db.sm_invoice_head.id.count(),groupby=db.sm_invoice_head.market_id)
    for headRec2 in headRecords2:
        market_id=headRec2.sm_invoice_head.market_id
        market_name=headRec2[db.sm_invoice_head.market_name.max()]
        market_count=headRec2[db.sm_invoice_head.id.count()]        
        if market_count>maxCount:
            maxMarketID=market_id
            maxmarketName=market_name
            maxCount=market_count
        else:
            continue
    
    #-------------------------    
    headRecords=qset.select(db.sm_invoice_head.client_id,db.sm_invoice_head.id.count(),db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),groupby=db.sm_invoice_head.client_id)
    clientCount=len(headRecords)
    
    #------------------    
    invoiceTotal=0
    totalDiscount=0
    totalSpDiscount=0
    actual_total_tp=0
    for hRow in headRecords:
        invoiceTotal+=hRow[db.sm_invoice_head.id.count()]
        actual_total_tp+=hRow[db.sm_invoice_head.actual_total_tp.sum()]
        totalDiscount+=hRow[db.sm_invoice_head.discount.sum()]
        totalSpDiscount+=hRow[db.sm_invoice_head.sp_discount.sum()]
        
    records2=qset((db.sm_invoice.cid==c_id) & (db.sm_invoice.depot_id==req_depot)&(db.sm_invoice_head.sl==db.sm_invoice.sl)).select(db.sm_invoice.level2_id,db.sm_invoice.item_id,db.sm_invoice.item_name.max(),db.sm_invoice.batch_id,db.sm_invoice.actual_tp,db.sm_invoice.price,db.sm_invoice.item_vat,db.sm_invoice.item_unit.max(),db.sm_invoice.quantity.sum(),db.sm_invoice.bonus_qty.sum(),orderby=db.sm_invoice.level2_id|db.sm_invoice.item_name|db.sm_invoice.batch_id|~db.sm_invoice.price,groupby=db.sm_invoice.level2_id|db.sm_invoice.item_id|db.sm_invoice.batch_id|db.sm_invoice.actual_tp|db.sm_invoice.price|db.sm_invoice.item_vat)      
    
    return dict(records=records,records2=records2,maxMarketID=maxMarketID,maxmarketName=maxmarketName,paymentMode=paymentMode,search_from_sl=search_from_sl,search_to_sl=search_to_sl,territory_id=territory_id,territory_name=territory_name,invoice_dateFrom=invoice_dateFrom,invoice_dateTo=invoice_dateTo,d_man_id=d_man_id,d_man_name=d_man_name,creditType=creditType,clientCount=clientCount,actual_total_tp=actual_total_tp,invoiceTotal=invoiceTotal,totalDiscount=totalDiscount,totalSpDiscount=totalSpDiscount)


#========================= Show Invoice invoice_list_synopsis
def invoice_synopsis_before_del_download():
    c_id=session.cid
    req_depot=session.depot_id
    
    #--------------- Title
    response.title='Download-Synopsis-Item List+Invoice Before delivery'
    #-------------
    
    #-----------
    invoice_dateFrom=''
    invoice_dateTo=''
    
    territory_id=''
    territory_name=''    
    
    d_man_id=''
    d_man_name=''
    paymentMode=''
    search_from_sl=''
    search_to_sl=''
    creditType=''
    #----------------------
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.sl!=0)
    qset=qset(db.sm_invoice_head.depot_id==req_depot)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    
    #----------
    if (session.btn_filter_printm_s):
        if session.search_dt_from!='' and session.search_dt_to!='':
            qset=qset((db.sm_invoice_head.invoice_date>=session.search_dt_from)&(db.sm_invoice_head.invoice_date<=session.search_dt_to))
            invoice_dateFrom=session.search_dt_from
            invoice_dateTo=session.search_dt_to
            
        if session.search_from_sl>0 and session.search_to_sl>0:
            qset=qset((db.sm_invoice_head.sl>=session.search_from_sl)&(db.sm_invoice_head.sl<=session.search_to_sl))
            search_from_sl=session.search_from_sl
            search_to_sl=session.search_to_sl
            
        #------------
        if (session.search_type_printm_s=='REPID'):                
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.rep_id==searchValue)
            
        elif (session.search_type_printm_s=='ROUTEID'):
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.area_id==searchValue)
            
            territory_id=searchValue
            if territory_id!='':
                areaRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id) & (db.sm_level.is_leaf == '1')).select(db.sm_level.level_name,db.sm_level.level0,db.sm_level.level0_name,limitby=(0,1))
                if areaRow:
                    territory_name=areaRow[0].level_name
                    
        elif (session.search_type_printm_s=='CLIENTID'):
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.client_id==searchValue)
        
        elif (session.search_type_printm_s=='SHIPMENT'):
            searchValue=str(session.search_value_printm_s).strip()
            qset=qset(db.sm_invoice_head.shipment_no==searchValue)
            
        #----------
        if session.print_status=='Pending':
            qset=qset(db.sm_invoice_head.field2==0)
            
        #----------
        if session.paymentMode!='':
            qset=qset(db.sm_invoice_head.payment_mode==session.paymentMode)
            paymentMode=session.paymentMode
            
        #----------
        if session.creditType!='':
            qset=qset(db.sm_invoice_head.credit_note==session.creditType)
            creditType=session.creditType
            
        #----------
        if not(session.d_man_id_report=='' or session.d_man_id_report==None):
            searchValue=str(session.d_man_id_report).split('|')[0]
            qset=qset(db.sm_invoice_head.d_man_id==searchValue)
            
            d_man_id=searchValue
            dmanRecords=db((db.sm_delivery_man.cid==c_id)& (db.sm_delivery_man.depot_id==req_depot) & (db.sm_delivery_man.d_man_id==d_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
            if dmanRecords:
                d_man_name=dmanRecords[0].name
                
    records=qset.select(db.sm_invoice_head.ALL,orderby=db.sm_invoice_head.sl)
    
    #---------------------- maximum market Name
    maxMarketID=''
    maxmarketName=''
    maxCount=0
    headRecords2=qset.select(db.sm_invoice_head.market_id,db.sm_invoice_head.market_name.max(),db.sm_invoice_head.id.count(),groupby=db.sm_invoice_head.market_id)
    for headRec2 in headRecords2:
        market_id=headRec2.sm_invoice_head.market_id
        market_name=headRec2[db.sm_invoice_head.market_name.max()]
        market_count=headRec2[db.sm_invoice_head.id.count()]        
        if market_count>maxCount:
            maxMarketID=market_id
            maxmarketName=market_name
            maxCount=market_count
        else:
            continue
    
    #-------------------------    
    headRecords=qset.select(db.sm_invoice_head.client_id,db.sm_invoice_head.id.count(),db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),groupby=db.sm_invoice_head.client_id)
    clientCount=len(headRecords)
    
    #------------------    
    invoiceTotal=0
    totalDiscount=0
    totalSpDiscount=0
    actual_total_tp=0
    for hRow in headRecords:
        invoiceTotal+=hRow[db.sm_invoice_head.id.count()]
        actual_total_tp+=hRow[db.sm_invoice_head.actual_total_tp.sum()]
        totalDiscount+=hRow[db.sm_invoice_head.discount.sum()]
        totalSpDiscount+=hRow[db.sm_invoice_head.sp_discount.sum()]
                
    records2=qset((db.sm_invoice.cid==c_id) & (db.sm_invoice.depot_id==req_depot)&(db.sm_invoice_head.sl==db.sm_invoice.sl)).select(db.sm_invoice.level2_id,db.sm_invoice.item_id,db.sm_invoice.item_name.max(),db.sm_invoice.batch_id,db.sm_invoice.actual_tp,db.sm_invoice.price,db.sm_invoice.item_vat,db.sm_invoice.item_unit.max(),db.sm_invoice.quantity.sum(),db.sm_invoice.bonus_qty.sum(),orderby=db.sm_invoice.level2_id|db.sm_invoice.item_name|db.sm_invoice.batch_id|~db.sm_invoice.price,groupby=db.sm_invoice.level2_id|db.sm_invoice.item_id|db.sm_invoice.batch_id|db.sm_invoice.actual_tp|db.sm_invoice.price|db.sm_invoice.item_vat)      
    
    #-------------------------    
    if paymentMode=='':
        termsStr='ALL'
    else:
        termsStr=paymentMode
        
        if paymentMode=='CREDIT':
            if creditType=='':
                termsStr+='(ALL)'
            else:
                termsStr+='('+creditType+')'
    
    
    myString='(5.3A) SYNOPSIS (Item List+Invoice List)-Before Delivery\n'
    myString+='SYNOPSIS (Before Delivery):,'+str(territory_id)+'\n'
    myString+='Market:,'+str(maxMarketID)+'|'+str(maxmarketName)+'\n'
    myString+='Delivery Person ID:,'+str(d_man_id)+'\n'
    myString+='Delivery Person Name:'+','+str(d_man_name)+'\n'
    myString+='Sales Term:,'+str(termsStr)+'\n'
    myString+='From Invoice:,'+str(search_from_sl)+'\n'
    myString+='To Invoice Range:'+','+str(search_to_sl)+'\n'
    myString+='From Date:,'+str(invoice_dateFrom)+'\n'
    myString+='To Date:,'+str(invoice_dateTo)+'\n'
    
    if territory_id!='':
        myString+=str(territory_id)+' Territory wise'+'\n'
    elif d_man_id!='':
        myString+='DP wise'+'\n'
        
    netTotal=0.0
    total_trade_price=0.0
    total_vat=0.0
    spDiscountTotal=0
    
    rowSl=0
    myString+='Sl.No,Item ID,Item Name,Batch No,Trade Price,Vat,Unit,Quantity,Bonus,Net Issue'+'\n'
    
    preArea=''    
    for record in records2:        
        newArea=record.sm_invoice.level2_id
        if preArea!=newArea:            
            myString+=str(newArea)+'\n'    
            rowSl=0            
        preArea=newArea
        rowSl+=1
        
        item_id=record.sm_invoice.item_id
        item_name=str(record[db.sm_invoice.item_name.max()]).replace(',', ' ')        
        batch_id=record.sm_invoice.batch_id
        itemRate=record.sm_invoice.price
        itemQty=record[db.sm_invoice.quantity.sum()]
        actualTp=record.sm_invoice.actual_tp
        
        spDiscount=(actualTp-itemRate)*itemQty
        if spDiscount < 0:
            spDiscount=0
        spDiscountTotal+=spDiscount
        
        item_vat=record.sm_invoice.item_vat
        item_unit=record[db.sm_invoice.item_unit.max()]
        
        total_trade_price+=actualTp*itemQty
        
        total_vat+=record.sm_invoice.item_vat*itemQty
        
        bonus_qty=record[db.sm_invoice.bonus_qty.sum()]
        totalQty=itemQty+record[db.sm_invoice.bonus_qty.sum()]
        
        #------------------------        
        myString+=str(rowSl)+','+str(item_id)+','+str(item_name)+','+str(batch_id)+','+str(actualTp)+','+str(item_vat)+','+str(item_unit)+','+str(itemQty)+','+str(bonus_qty)+','+str(totalQty)+'\n'
    
    myString+='\nSummary,,,,,,,,,,,,,,,,,,,,\n'
    
    myString+='Total Trade Price:,'+str(round(total_trade_price,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='VAT:,'+str(round(total_vat,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Total Trade Concession Amount:,'+str(round(totalDiscount,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Special Discount,'+str(round(spDiscountTotal,2))+',,,,,,,,,,,,,,,,,,,\n'
    netTotal=total_trade_price+total_vat-(totalDiscount+spDiscountTotal)
    myString+='Net Total:,'+str(round(netTotal,2))+',,,,,,,,,,,,,,,,,,,\n\n'
    
    inwordStr=num2word(str(round(netTotal,2)))
    
    myString+='Net Sales (Taka in Words):,'+str(inwordStr)+',,,,,,,,,,,,,,,,,,,\n'
    
    myString+='Total Invoice:,'+str(invoiceTotal)+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Total Customer:,'+str(clientCount)+',,,,,,,,,,,,,,,,,,,\n'
    
    myString+='\n\n\n\n'
    
    myString+='SYNOPSIS (Invoice List)-Before Delivery:,'+str(territory_id)+'\n'
    myString+='Market:,'+str(maxMarketID)+'|'+str(maxmarketName)+'\n'
    myString+='Delivery Person ID:,'+str(d_man_id)+'\n'
    myString+='Delivery Person Name:'+','+str(d_man_name)+'\n'
    myString+='Sales Term:,'+str(termsStr)+'\n'
    myString+='From Invoice:,'+str(search_from_sl)+'\n'
    myString+='To Invoice Range:'+','+str(search_to_sl)+'\n'
    myString+='From Date:,'+str(invoice_dateFrom)+'\n'
    myString+='To Date:,'+str(invoice_dateTo)+'\n'
    
    if territory_id!='':
        myString+=str(territory_id)+' Territory wise'+'\n'
    elif d_man_id!='':
        myString+='DP wise'+'\n'
    
    
    invoice_total_tp=0.0
    vat_total=0.0
    discount_total=0.0
    totalSpAmt=0.0
    netInvAmt_total=0.0    
    netTotalOS=0.0
    totalOs=0
    
    rowSl=0
    myString+='Sl.No,Invoice No,Invoice Date,Cust.ID,Customer Name,TP,VAT,Disc,Sp.Disc,Invocie Net,Previous O/S,Total O/S,Credit Limit'+'\n'
    for record in records:
        rowSl+=1        
        invNo=str(session.prefix_invoice)+'INV'+str(record.depot_id)+'-'+str(record.sl)                                                           
        invoice_date=record.invoice_date
        client_id=record.client_id
        client_name=str(record.client_name).replace(',', ' ')        
        invTpAmt=round(record.actual_total_tp,2)
        invoice_total_tp+=invTpAmt
        vatAmt=round(record.vat_total_amount,2)
        vat_total+=vatAmt
        discountAmt=round(record.discount,2)
        discount_total+=discountAmt
        spAmt=round(record.sp_discount,2)
        totalSpAmt+=spAmt
        netInvAmt=round(invTpAmt+vatAmt-(discountAmt+spAmt),2)
        netInvAmt_total+=netInvAmt
        
        osAmt=round(record.previous_ost_amt,2)
        totalOs+=osAmt
        
        netOstAmt=round(netInvAmt+osAmt,2)
        netTotalOS+=netOstAmt
        
        client_limit_amt=record.client_limit_amt
        
        #------------------------        
        myString+=str(rowSl)+','+str(invNo)+','+str(invoice_date)+','+str(client_id)+','+str(client_name)+','+str(invTpAmt)+','+str(vatAmt)+','+str(discountAmt)+','+str(spAmt)+','+str(netInvAmt)+','+str(osAmt)+','+str(netOstAmt)+','+str(client_limit_amt)+'\n'
    
    myString+='Total:,,,,,'+str(invoice_total_tp)+','+str(vat_total)+','+str(discount_total)+','+str(totalSpAmt)+','+str(netInvAmt_total)+','+str(totalOs)+','+str(netTotalOS)+'\n'
    
    
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_synopsisInvoiceAndItemListBeforeDelivery.csv'   
    return str(myString)

    
    return dict(records=records,records2=records2,maxMarketID=maxMarketID,maxmarketName=maxmarketName,paymentMode=paymentMode,search_from_sl=search_from_sl,search_to_sl=search_to_sl,territory_id=territory_id,territory_name=territory_name,invoice_dateFrom=invoice_dateFrom,invoice_dateTo=invoice_dateTo,d_man_id=d_man_id,d_man_name=d_man_name,creditType=creditType,clientCount=clientCount,actual_total_tp=actual_total_tp,invoiceTotal=invoiceTotal,totalDiscount=totalDiscount,totalSpDiscount=totalSpDiscount)


def invoice_synopsis_before_del_withoutbatch():
    c_id=session.cid
    req_depot=session.depot_id
    
    #--------------- Title
    response.title='5.3B Synopsis-Item List+Invoice Before delivery'
    #-------------
    
    #-----------
    invoice_dateFrom=''
    invoice_dateTo=''
    
    territory_id=''
    territory_name=''    
    
    d_man_id=''
    d_man_name=''
    paymentMode=''
    search_from_sl=''
    search_to_sl=''
    creditType=''
    #----------------------
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.sl!=0)
    qset=qset(db.sm_invoice_head.depot_id==req_depot)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    
    #----------
    if (session.btn_filter_printm_s):
        if session.search_dt_from!='' and session.search_dt_to!='':
            qset=qset((db.sm_invoice_head.invoice_date>=session.search_dt_from)&(db.sm_invoice_head.invoice_date<=session.search_dt_to))
            invoice_dateFrom=session.search_dt_from
            invoice_dateTo=session.search_dt_to
            
        if session.search_from_sl>0 and session.search_to_sl>0:
            qset=qset((db.sm_invoice_head.sl>=session.search_from_sl)&(db.sm_invoice_head.sl<=session.search_to_sl))
            search_from_sl=session.search_from_sl
            search_to_sl=session.search_to_sl
            
        #------------
        if (session.search_type_printm_s=='REPID'):                
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.rep_id==searchValue)
            
        elif (session.search_type_printm_s=='ROUTEID'):
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.area_id==searchValue)
            
            territory_id=searchValue
            if territory_id!='':
                areaRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id) & (db.sm_level.is_leaf == '1')).select(db.sm_level.level_name,db.sm_level.level0,db.sm_level.level0_name,limitby=(0,1))
                if areaRow:
                    territory_name=areaRow[0].level_name
                    
        elif (session.search_type_printm_s=='CLIENTID'):
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.client_id==searchValue)
        
        elif (session.search_type_printm_s=='SHIPMENT'):
            searchValue=str(session.search_value_printm_s).strip()
            qset=qset(db.sm_invoice_head.shipment_no==searchValue)
            
        #----------
        if session.print_status=='Pending':
            qset=qset(db.sm_invoice_head.field2==0)
            
        #----------
        if session.paymentMode!='':
            qset=qset(db.sm_invoice_head.payment_mode==session.paymentMode)
            paymentMode=session.paymentMode
            
        #----------
        if session.creditType!='':
            qset=qset(db.sm_invoice_head.credit_note==session.creditType)
            creditType=session.creditType
            
        #----------
        if not(session.d_man_id_report=='' or session.d_man_id_report==None):
            searchValue=str(session.d_man_id_report).split('|')[0]
            qset=qset(db.sm_invoice_head.d_man_id==searchValue)
            
            d_man_id=searchValue
            dmanRecords=db((db.sm_delivery_man.cid==c_id)& (db.sm_delivery_man.depot_id==req_depot) & (db.sm_delivery_man.d_man_id==d_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
            if dmanRecords:
                d_man_name=dmanRecords[0].name
                
    records=qset.select(db.sm_invoice_head.ALL,orderby=db.sm_invoice_head.sl)
    
    #---------------------- maximum market Name
    maxMarketID=''
    maxmarketName=''
    maxCount=0
    headRecords2=qset.select(db.sm_invoice_head.market_id,db.sm_invoice_head.market_name.max(),db.sm_invoice_head.id.count(),groupby=db.sm_invoice_head.market_id)
    for headRec2 in headRecords2:
        market_id=headRec2.sm_invoice_head.market_id
        market_name=headRec2[db.sm_invoice_head.market_name.max()]
        market_count=headRec2[db.sm_invoice_head.id.count()]        
        if market_count>maxCount:
            maxMarketID=market_id
            maxmarketName=market_name
            maxCount=market_count
        else:
            continue
    
    #-------------------------    
    headRecords=qset.select(db.sm_invoice_head.client_id,db.sm_invoice_head.id.count(),db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),groupby=db.sm_invoice_head.client_id)
    clientCount=len(headRecords)
    
    #------------------    
    invoiceTotal=0
    totalDiscount=0
    totalSpDiscount=0
    actual_total_tp=0
    for hRow in headRecords:
        invoiceTotal+=hRow[db.sm_invoice_head.id.count()]
        actual_total_tp+=hRow[db.sm_invoice_head.actual_total_tp.sum()]
        totalDiscount+=hRow[db.sm_invoice_head.discount.sum()]
        totalSpDiscount+=hRow[db.sm_invoice_head.sp_discount.sum()]
        
    records2=qset((db.sm_invoice.cid==c_id) & (db.sm_invoice.depot_id==req_depot)&(db.sm_invoice_head.sl==db.sm_invoice.sl)).select(db.sm_invoice.item_id,db.sm_invoice.item_name.max(),db.sm_invoice.actual_tp,db.sm_invoice.price,db.sm_invoice.item_vat,db.sm_invoice.item_unit.max(),db.sm_invoice.quantity.sum(),db.sm_invoice.bonus_qty.sum(),orderby=db.sm_invoice.item_name|~db.sm_invoice.price,groupby=db.sm_invoice.item_id|db.sm_invoice.actual_tp|db.sm_invoice.price|db.sm_invoice.item_vat)      
    
    return dict(records=records,records2=records2,maxMarketID=maxMarketID,maxmarketName=maxmarketName,paymentMode=paymentMode,search_from_sl=search_from_sl,search_to_sl=search_to_sl,territory_id=territory_id,territory_name=territory_name,invoice_dateFrom=invoice_dateFrom,invoice_dateTo=invoice_dateTo,d_man_id=d_man_id,d_man_name=d_man_name,creditType=creditType,clientCount=clientCount,actual_total_tp=actual_total_tp,invoiceTotal=invoiceTotal,totalDiscount=totalDiscount,totalSpDiscount=totalSpDiscount)


#========================= Show Invoice invoice_list_synopsis
def invoice_synopsis_before_del_withoutbatch_download():
    c_id=session.cid
    req_depot=session.depot_id
    
    #--------------- Title
    response.title='Download-Synopsis-Item List+Invoice List Before delivery'
    #-------------
    
    #-----------
    invoice_dateFrom=''
    invoice_dateTo=''
    
    territory_id=''
    territory_name=''    
    
    d_man_id=''
    d_man_name=''
    paymentMode=''
    search_from_sl=''
    search_to_sl=''
    creditType=''
    #----------------------
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.sl!=0)
    qset=qset(db.sm_invoice_head.depot_id==req_depot)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    
    #----------
    if (session.btn_filter_printm_s):
        if session.search_dt_from!='' and session.search_dt_to!='':
            qset=qset((db.sm_invoice_head.invoice_date>=session.search_dt_from)&(db.sm_invoice_head.invoice_date<=session.search_dt_to))
            invoice_dateFrom=session.search_dt_from
            invoice_dateTo=session.search_dt_to
            
        if session.search_from_sl>0 and session.search_to_sl>0:
            qset=qset((db.sm_invoice_head.sl>=session.search_from_sl)&(db.sm_invoice_head.sl<=session.search_to_sl))
            search_from_sl=session.search_from_sl
            search_to_sl=session.search_to_sl
            
        #------------
        if (session.search_type_printm_s=='REPID'):                
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.rep_id==searchValue)
            
        elif (session.search_type_printm_s=='ROUTEID'):
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.area_id==searchValue)
            
            territory_id=searchValue
            if territory_id!='':
                areaRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id) & (db.sm_level.is_leaf == '1')).select(db.sm_level.level_name,db.sm_level.level0,db.sm_level.level0_name,limitby=(0,1))
                if areaRow:
                    territory_name=areaRow[0].level_name
                    
        elif (session.search_type_printm_s=='CLIENTID'):
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.client_id==searchValue)
        
        elif (session.search_type_printm_s=='SHIPMENT'):
            searchValue=str(session.search_value_printm_s).strip()
            qset=qset(db.sm_invoice_head.shipment_no==searchValue)
            
        #----------
        if session.print_status=='Pending':
            qset=qset(db.sm_invoice_head.field2==0)
            
        #----------
        if session.paymentMode!='':
            qset=qset(db.sm_invoice_head.payment_mode==session.paymentMode)
            paymentMode=session.paymentMode
            
        #----------
        if session.creditType!='':
            qset=qset(db.sm_invoice_head.credit_note==session.creditType)
            creditType=session.creditType
            
        #----------
        if not(session.d_man_id_report=='' or session.d_man_id_report==None):
            searchValue=str(session.d_man_id_report).split('|')[0]
            qset=qset(db.sm_invoice_head.d_man_id==searchValue)
            
            d_man_id=searchValue
            dmanRecords=db((db.sm_delivery_man.cid==c_id)& (db.sm_delivery_man.depot_id==req_depot) & (db.sm_delivery_man.d_man_id==d_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
            if dmanRecords:
                d_man_name=dmanRecords[0].name
                
    records=qset.select(db.sm_invoice_head.ALL,orderby=db.sm_invoice_head.sl)
    
    #---------------------- maximum market Name
    maxMarketID=''
    maxmarketName=''
    maxCount=0
    headRecords2=qset.select(db.sm_invoice_head.market_id,db.sm_invoice_head.market_name.max(),db.sm_invoice_head.id.count(),groupby=db.sm_invoice_head.market_id)
    for headRec2 in headRecords2:
        market_id=headRec2.sm_invoice_head.market_id
        market_name=headRec2[db.sm_invoice_head.market_name.max()]
        market_count=headRec2[db.sm_invoice_head.id.count()]        
        if market_count>maxCount:
            maxMarketID=market_id
            maxmarketName=market_name
            maxCount=market_count
        else:
            continue
    
    #-------------------------    
    headRecords=qset.select(db.sm_invoice_head.client_id,db.sm_invoice_head.id.count(),db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),groupby=db.sm_invoice_head.client_id)
    clientCount=len(headRecords)
    
    #------------------    
    invoiceTotal=0
    totalDiscount=0
    totalSpDiscount=0
    actual_total_tp=0
    for hRow in headRecords:
        invoiceTotal+=hRow[db.sm_invoice_head.id.count()]
        actual_total_tp+=hRow[db.sm_invoice_head.actual_total_tp.sum()]
        totalDiscount+=hRow[db.sm_invoice_head.discount.sum()]
        totalSpDiscount+=hRow[db.sm_invoice_head.sp_discount.sum()]
        
    records2=qset((db.sm_invoice.cid==c_id) & (db.sm_invoice.depot_id==req_depot)&(db.sm_invoice_head.sl==db.sm_invoice.sl)).select(db.sm_invoice.item_id,db.sm_invoice.item_name.max(),db.sm_invoice.actual_tp,db.sm_invoice.price,db.sm_invoice.item_vat,db.sm_invoice.item_unit.max(),db.sm_invoice.quantity.sum(),db.sm_invoice.bonus_qty.sum(),orderby=db.sm_invoice.item_name|~db.sm_invoice.price,groupby=db.sm_invoice.item_id|db.sm_invoice.actual_tp|db.sm_invoice.price|db.sm_invoice.item_vat)      
    
    #-------------------------    
    if paymentMode=='':
        termsStr='ALL'
    else:
        termsStr=paymentMode
        
        if paymentMode=='CREDIT':
            if creditType=='':
                termsStr+='(ALL)'
            else:
                termsStr+='('+creditType+')'
    
    
    myString='(5.3B) SYNOPSIS (Item List+Invoice List)Without Batch-Before Delivery\n'
    myString+='SYNOPSIS (Before Delivery):,'+str(territory_id)+'\n'
    myString+='Market:,'+str(maxMarketID)+'|'+str(maxmarketName)+'\n'
    myString+='Delivery Person ID:,'+str(d_man_id)+'\n'
    myString+='Delivery Person Name:'+','+str(d_man_name)+'\n'
    myString+='Sales Term:,'+str(termsStr)+'\n'
    myString+='From Invoice:,'+str(search_from_sl)+'\n'
    myString+='To Invoice Range:'+','+str(search_to_sl)+'\n'
    myString+='From Date:,'+str(invoice_dateFrom)+'\n'
    myString+='To Date:,'+str(invoice_dateTo)+'\n'
    
    if territory_id!='':
        myString+=str(territory_id)+' Territory wise'+'\n'
    elif d_man_id!='':
        myString+='DP wise'+'\n'
        
    netTotal=0.0
    total_trade_price=0.0
    total_vat=0.0
    spDiscountTotal=0
    
    rowSl=0
    myString+='Sl.No,Item ID,Item Name,Trade Price,Vat,Unit,Quantity,Bonus,Net Issue'+'\n'
    
    preArea=''    
    for record in records2:        
#         newArea=record.sm_invoice.level2_id
#         if preArea!=newArea:            
#             myString+=str(newArea)+'\n'    
#             rowSl=0            
#         preArea=newArea
        rowSl+=1
        
        item_id=record.sm_invoice.item_id
        item_name=str(record[db.sm_invoice.item_name.max()]).replace(',', ' ')        
        
        itemRate=record.sm_invoice.price
        itemQty=record[db.sm_invoice.quantity.sum()]
        actualTp=record.sm_invoice.actual_tp
        
        spDiscount=(actualTp-itemRate)*itemQty
        if spDiscount < 0:
            spDiscount=0
        spDiscountTotal+=spDiscount
        
        item_vat=record.sm_invoice.item_vat
        item_unit=record[db.sm_invoice.item_unit.max()]
        
        total_trade_price+=actualTp*itemQty
        
        total_vat+=record.sm_invoice.item_vat*itemQty
        
        bonus_qty=record[db.sm_invoice.bonus_qty.sum()]
        totalQty=itemQty+record[db.sm_invoice.bonus_qty.sum()]
        
        #------------------------        
        myString+=str(rowSl)+','+str(item_id)+','+str(item_name)+','+str(actualTp)+','+str(item_vat)+','+str(item_unit)+','+str(itemQty)+','+str(bonus_qty)+','+str(totalQty)+'\n'
    
    myString+='\nSummary,,,,,,,,,,,,,,,,,,,,\n'
    
    myString+='Total Trade Price:,'+str(round(total_trade_price,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='VAT:,'+str(round(total_vat,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Total Trade Concession Amount:,'+str(round(totalDiscount,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Special Discount,'+str(round(spDiscountTotal,2))+',,,,,,,,,,,,,,,,,,,\n'
    netTotal=total_trade_price+total_vat-(totalDiscount+spDiscountTotal)
    myString+='Net Total:,'+str(round(netTotal,2))+',,,,,,,,,,,,,,,,,,,\n\n'
    
    inwordStr=num2word(str(round(netTotal,2)))
    
    myString+='Net Sales (Taka in Words):,'+str(inwordStr)+',,,,,,,,,,,,,,,,,,,\n'
    
    myString+='Total Invoice:,'+str(invoiceTotal)+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Total Customer:,'+str(clientCount)+',,,,,,,,,,,,,,,,,,,\n'
    
    myString+='\n\n\n\n'
    
    myString+='SYNOPSIS (Invoice List)-Before Delivery:,'+str(territory_id)+'\n'
    myString+='Market:,'+str(maxMarketID)+'|'+str(maxmarketName)+'\n'
    myString+='Delivery Person ID:,'+str(d_man_id)+'\n'
    myString+='Delivery Person Name:'+','+str(d_man_name)+'\n'
    myString+='Sales Term:,'+str(termsStr)+'\n'
    myString+='From Invoice:,'+str(search_from_sl)+'\n'
    myString+='To Invoice Range:'+','+str(search_to_sl)+'\n'
    myString+='From Date:,'+str(invoice_dateFrom)+'\n'
    myString+='To Date:,'+str(invoice_dateTo)+'\n'
    
    if territory_id!='':
        myString+=str(territory_id)+' Territory wise'+'\n'
    elif d_man_id!='':
        myString+='DP wise'+'\n'
    
    
    invoice_total_tp=0.0
    vat_total=0.0
    discount_total=0.0
    totalSpAmt=0.0
    netInvAmt_total=0.0    
    netTotalOS=0.0
    totalOs=0
    
    rowSl=0
    myString+='Sl.No,Invoice No,Invoice Date,Cust.ID,Customer Name,TP,VAT,Disc,Sp.Disc,Invocie Net,Previous O/S,Total O/S,Credit Limit'+'\n'
    for record in records:
        rowSl+=1        
        invNo=str(session.prefix_invoice)+'INV'+str(record.depot_id)+'-'+str(record.sl)                                                           
        invoice_date=record.invoice_date
        client_id=record.client_id
        client_name=str(record.client_name).replace(',', ' ')        
        invTpAmt=round(record.actual_total_tp,2)
        invoice_total_tp+=invTpAmt
        vatAmt=round(record.vat_total_amount,2)
        vat_total+=vatAmt
        discountAmt=round(record.discount,2)
        discount_total+=discountAmt
        spAmt=round(record.sp_discount,2)
        totalSpAmt+=spAmt
        netInvAmt=round(invTpAmt+vatAmt-(discountAmt+spAmt),2)
        netInvAmt_total+=netInvAmt
        
        osAmt=round(record.previous_ost_amt,2)
        totalOs+=osAmt
        
        netOstAmt=round(netInvAmt+osAmt,2)
        netTotalOS+=netOstAmt
        
        client_limit_amt=record.client_limit_amt
        
        #------------------------        
        myString+=str(rowSl)+','+str(invNo)+','+str(invoice_date)+','+str(client_id)+','+str(client_name)+','+str(invTpAmt)+','+str(vatAmt)+','+str(discountAmt)+','+str(spAmt)+','+str(netInvAmt)+','+str(osAmt)+','+str(netOstAmt)+','+str(client_limit_amt)+'\n'
    
    myString+='Total:,,,,,'+str(invoice_total_tp)+','+str(vat_total)+','+str(discount_total)+','+str(totalSpAmt)+','+str(netInvAmt_total)+','+str(totalOs)+','+str(netTotalOS)+'\n'
    
    
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_synopsisInvoiceAndItemListBeforeDelivery.csv'   
    return str(myString)

    
    return dict(records=records,records2=records2,maxMarketID=maxMarketID,maxmarketName=maxmarketName,paymentMode=paymentMode,search_from_sl=search_from_sl,search_to_sl=search_to_sl,territory_id=territory_id,territory_name=territory_name,invoice_dateFrom=invoice_dateFrom,invoice_dateTo=invoice_dateTo,d_man_id=d_man_id,d_man_name=d_man_name,creditType=creditType,clientCount=clientCount,actual_total_tp=actual_total_tp,invoiceTotal=invoiceTotal,totalDiscount=totalDiscount,totalSpDiscount=totalSpDiscount)


#========================= Show Invoice invoice_list_synopsis
def invoice_list_synopsis_bak():
    c_id=session.cid
    req_depot=session.depot_id
    
    #--------------- Title
    response.title='Synopsis - Invoice List'
    #-------------
    
    #-----------
    invoice_dateFrom=''
    invoice_dateTo=''
    
    territory_id=''
    territory_name=''    
    
    d_man_id=''
    d_man_name=''
    paymentMode=''
    search_from_sl=''
    search_to_sl=''
    creditType=''
    #----------------------
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.sl!=0)
    qset=qset(db.sm_invoice_head.depot_id==req_depot)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    
    #----------
    if (session.btn_filter_printm_s):
        if session.search_dt_from!='' and session.search_dt_to!='':
            qset=qset((db.sm_invoice_head.invoice_date>=session.search_dt_from)&(db.sm_invoice_head.invoice_date<=session.search_dt_to))
            invoice_dateFrom=session.search_dt_from
            invoice_dateTo=session.search_dt_to
            
        if session.search_from_sl>0 and session.search_to_sl>0:
            qset=qset((db.sm_invoice_head.sl>=session.search_from_sl)&(db.sm_invoice_head.sl<=session.search_to_sl))
            search_from_sl=session.search_from_sl
            search_to_sl=session.search_to_sl
            
        #------------
        if (session.search_type_printm_s=='REPID'):                
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.rep_id==searchValue)
            
        elif (session.search_type_printm_s=='ROUTEID'):
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.area_id==searchValue)
            
            territory_id=searchValue
            if territory_id!='':
                areaRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id) & (db.sm_level.is_leaf == '1')).select(db.sm_level.level_name,db.sm_level.level0,db.sm_level.level0_name,limitby=(0,1))
                if areaRow:
                    territory_name=areaRow[0].level_name
                    
        elif (session.search_type_printm_s=='CLIENTID'):
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.client_id==searchValue)
        
        elif (session.search_type_printm_s=='SHIPMENT'):
            searchValue=str(session.search_value_printm_s).strip()
            qset=qset(db.sm_invoice_head.shipment_no==searchValue)
            
        #----------
        if session.print_status=='Pending':
            qset=qset(db.sm_invoice_head.field2==0)
            
        #----------
        if session.paymentMode!='':
            qset=qset(db.sm_invoice_head.payment_mode==session.paymentMode)
            paymentMode=session.paymentMode
            
        #----------
        if session.creditType!='':
            qset=qset(db.sm_invoice_head.credit_note==session.creditType)
            creditType=session.creditType
            
        #----------
        if not(session.d_man_id_report=='' or session.d_man_id_report==None):
            searchValue=str(session.d_man_id_report).split('|')[0]
            qset=qset(db.sm_invoice_head.d_man_id==searchValue)
            
            d_man_id=searchValue
            dmanRecords=db((db.sm_delivery_man.cid==c_id)& (db.sm_delivery_man.depot_id==req_depot) & (db.sm_delivery_man.d_man_id==d_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
            if dmanRecords:
                d_man_name=dmanRecords[0].name
                
    records=qset.select(db.sm_invoice_head.ALL,orderby=db.sm_invoice_head.sl)
    
    #---------------------- maximum market Name
    maxMarketID=''
    maxmarketName=''
    maxCount=0
    headRecords2=qset.select(db.sm_invoice_head.market_id,db.sm_invoice_head.market_name.max(),db.sm_invoice_head.id.count(),groupby=db.sm_invoice_head.market_id)
    for headRec2 in headRecords2:
        market_id=headRec2.sm_invoice_head.market_id
        market_name=headRec2[db.sm_invoice_head.market_name.max()]
        market_count=headRec2[db.sm_invoice_head.id.count()]        
        if market_count>maxCount:
            maxMarketID=market_id
            maxmarketName=market_name
            maxCount=market_count
        else:
            continue
    
    #-------------------------
    return dict(records=records,maxMarketID=maxMarketID,maxmarketName=maxmarketName,paymentMode=paymentMode,search_from_sl=search_from_sl,search_to_sl=search_to_sl,territory_id=territory_id,territory_name=territory_name,invoice_dateFrom=invoice_dateFrom,invoice_dateTo=invoice_dateTo,d_man_id=d_man_id,d_man_name=d_man_name,creditType=creditType)

#========================= Show Invoice invoice_item_list_synopsis before delivery
def invoice_item_list_synopsis():
    c_id=session.cid
    req_depot=session.depot_id
    
    #--------------- Title
    response.title='5.3 Preview Invoice Item List With Batch'
    
    #-------------
    invoice_dateFrom=''
    invoice_dateTo=''
    
    territory_id=''
    territory_name=''    
    
    d_man_id=''
    d_man_name=''
    paymentMode=''
    search_from_sl=''
    search_to_sl=''
    creditType=''
    #----------------------
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.sl!=0)
    qset=qset(db.sm_invoice_head.depot_id==req_depot)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    
    #----------
    if (session.btn_filter_printm_s):
        if session.search_dt_from!='' and session.search_dt_to!='':
            qset=qset((db.sm_invoice_head.invoice_date>=session.search_dt_from)&(db.sm_invoice_head.invoice_date<=session.search_dt_to))
            invoice_dateFrom=session.search_dt_from
            invoice_dateTo=session.search_dt_to
            
        if session.search_from_sl>0 and session.search_to_sl>0:
            qset=qset((db.sm_invoice_head.sl>=session.search_from_sl)&(db.sm_invoice_head.sl<=session.search_to_sl))
            search_from_sl=session.search_from_sl
            search_to_sl=session.search_to_sl
            
        #------------
        if (session.search_type_printm_s=='REPID'):                
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.rep_id==searchValue)
            
        elif (session.search_type_printm_s=='ROUTEID'):
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.area_id==searchValue)
            
            territory_id=searchValue
            if territory_id!='':
                areaRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id) & (db.sm_level.is_leaf == '1')).select(db.sm_level.level_name,db.sm_level.level0,db.sm_level.level0_name,limitby=(0,1))
                if areaRow:
                    territory_name=areaRow[0].level_name
                    
        elif (session.search_type_printm_s=='CLIENTID'):
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.client_id==searchValue)
            
        elif (session.search_type_printm_s=='SHIPMENT'):
            searchValue=str(session.search_value_printm_s).strip()
            qset=qset(db.sm_invoice_head.shipment_no==searchValue)
            
        #----------
        if session.print_status=='Pending':
            qset=qset(db.sm_invoice_head.field2==0)
            
        #----------
        if session.paymentMode!='':
            qset=qset(db.sm_invoice_head.payment_mode==session.paymentMode)
            paymentMode=session.paymentMode
            
        #----------
        if session.creditType!='':
            qset=qset(db.sm_invoice_head.credit_note==session.creditType)
            creditType=session.creditType
            
        #----------
        if not(session.d_man_id_report=='' or session.d_man_id_report==None):
            searchValue=str(session.d_man_id_report).split('|')[0]
            qset=qset(db.sm_invoice_head.d_man_id==searchValue)
            
            d_man_id=searchValue
            dmanRecords=db((db.sm_delivery_man.cid==c_id)& (db.sm_delivery_man.depot_id==req_depot) & (db.sm_delivery_man.d_man_id==d_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
            if dmanRecords:
                d_man_name=dmanRecords[0].name
    
    headRecords=qset.select(db.sm_invoice_head.client_id,db.sm_invoice_head.id.count(),db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),groupby=db.sm_invoice_head.client_id)
    clientCount=len(headRecords)
    
    #---------------------- maximum market Name
    maxMarketID=''
    maxmarketName=''
    maxCount=0
    headRecords2=qset.select(db.sm_invoice_head.market_id,db.sm_invoice_head.market_name.max(),db.sm_invoice_head.id.count(),groupby=db.sm_invoice_head.market_id)
    for headRec2 in headRecords2:
        market_id=headRec2.sm_invoice_head.market_id
        market_name=headRec2[db.sm_invoice_head.market_name.max()]
        market_count=headRec2[db.sm_invoice_head.id.count()]        
        if market_count>maxCount:
            maxMarketID=market_id
            maxmarketName=market_name
            maxCount=market_count
        else:
            continue
    #------------------
    
    invoiceTotal=0
    totalDiscount=0
    totalSpDiscount=0
    actual_total_tp=0
    for hRow in headRecords:
        invoiceTotal+=hRow[db.sm_invoice_head.id.count()]
        actual_total_tp+=hRow[db.sm_invoice_head.actual_total_tp.sum()]
        totalDiscount+=hRow[db.sm_invoice_head.discount.sum()]
        totalSpDiscount+=hRow[db.sm_invoice_head.sp_discount.sum()]
        #& (db.sm_invoice.quantity>0)
    
    records=qset((db.sm_invoice.cid==c_id) & (db.sm_invoice.depot_id==req_depot)&(db.sm_invoice_head.sl==db.sm_invoice.sl)).select(db.sm_invoice.level2_id,db.sm_invoice.item_id,db.sm_invoice.item_name.max(),db.sm_invoice.batch_id,db.sm_invoice.actual_tp,db.sm_invoice.price,db.sm_invoice.item_vat,db.sm_invoice.item_unit.max(),db.sm_invoice.quantity.sum(),db.sm_invoice.bonus_qty.sum(),orderby=db.sm_invoice.level2_id|db.sm_invoice.item_name|db.sm_invoice.batch_id|~db.sm_invoice.price,groupby=db.sm_invoice.level2_id|db.sm_invoice.item_id|db.sm_invoice.batch_id|db.sm_invoice.actual_tp|db.sm_invoice.price|db.sm_invoice.item_vat)      
    
    #-------------------------
    return dict(records=records,maxMarketID=maxMarketID,maxmarketName=maxmarketName,paymentMode=paymentMode,creditType=creditType,search_from_sl=search_from_sl,search_to_sl=search_to_sl,territory_id=territory_id,territory_name=territory_name,invoice_dateFrom=invoice_dateFrom,invoice_dateTo=invoice_dateTo,d_man_id=d_man_id,d_man_name=d_man_name,clientCount=clientCount,actual_total_tp=actual_total_tp,invoiceTotal=invoiceTotal,totalDiscount=totalDiscount,totalSpDiscount=totalSpDiscount)
    

#========================= Show Invoice invoice_item_list_synopsis before delivery
def invoice_item_list_synopsis_download():
    c_id=session.cid
    req_depot=session.depot_id
    
    #-------------    
    invoice_dateFrom=''
    invoice_dateTo=''
    
    territory_id=''
    territory_name=''    
    
    d_man_id=''
    d_man_name=''
    paymentMode=''
    search_from_sl=''
    search_to_sl=''
    creditType=''
    #----------------------
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.sl!=0)
    qset=qset(db.sm_invoice_head.depot_id==req_depot)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    
    #----------
    if (session.btn_filter_printm_s):
        if session.search_dt_from!='' and session.search_dt_to!='':
            qset=qset((db.sm_invoice_head.invoice_date>=session.search_dt_from)&(db.sm_invoice_head.invoice_date<=session.search_dt_to))
            invoice_dateFrom=session.search_dt_from
            invoice_dateTo=session.search_dt_to
            
        if session.search_from_sl>0 and session.search_to_sl>0:
            qset=qset((db.sm_invoice_head.sl>=session.search_from_sl)&(db.sm_invoice_head.sl<=session.search_to_sl))
            search_from_sl=session.search_from_sl
            search_to_sl=session.search_to_sl
            
        #------------
        if (session.search_type_printm_s=='REPID'):                
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.rep_id==searchValue)
            
        elif (session.search_type_printm_s=='ROUTEID'):
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.area_id==searchValue)
            
            territory_id=searchValue
            if territory_id!='':
                areaRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id) & (db.sm_level.is_leaf == '1')).select(db.sm_level.level_name,db.sm_level.level0,db.sm_level.level0_name,limitby=(0,1))
                if areaRow:
                    territory_name=areaRow[0].level_name
                    
        elif (session.search_type_printm_s=='CLIENTID'):
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.client_id==searchValue)
        
        elif (session.search_type_printm_s=='SHIPMENT'):
            searchValue=str(session.search_value_printm_s).strip()
            qset=qset(db.sm_invoice_head.shipment_no==searchValue)
        
        #----------
        if session.print_status=='Pending':
            qset=qset(db.sm_invoice_head.field2==0)
            
        #----------
        if session.paymentMode!='':
            qset=qset(db.sm_invoice_head.payment_mode==session.paymentMode)
            paymentMode=session.paymentMode
            
        #----------
        if session.creditType!='':
            qset=qset(db.sm_invoice_head.credit_note==session.creditType)
            creditType=session.creditType
            
        #----------
        if not(session.d_man_id_report=='' or session.d_man_id_report==None):
            searchValue=str(session.d_man_id_report).split('|')[0]
            qset=qset(db.sm_invoice_head.d_man_id==searchValue)
            
            d_man_id=searchValue
            dmanRecords=db((db.sm_delivery_man.cid==c_id)& (db.sm_delivery_man.depot_id==req_depot) & (db.sm_delivery_man.d_man_id==d_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
            if dmanRecords:
                d_man_name=dmanRecords[0].name
    
    headRecords=qset.select(db.sm_invoice_head.client_id,db.sm_invoice_head.id.count(),db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),groupby=db.sm_invoice_head.client_id)
    clientCount=len(headRecords)
    #---------------------- maximum market Name
    maxMarketID=''
    maxmarketName=''
    maxCount=0
    headRecords2=qset.select(db.sm_invoice_head.market_id,db.sm_invoice_head.market_name.max(),db.sm_invoice_head.id.count(),groupby=db.sm_invoice_head.market_id)
    for headRec2 in headRecords2:
        market_id=headRec2.sm_invoice_head.market_id
        market_name=headRec2[db.sm_invoice_head.market_name.max()]
        market_count=headRec2[db.sm_invoice_head.id.count()]        
        if market_count>maxCount:
            maxMarketID=market_id
            maxmarketName=market_name
            maxCount=market_count
        else:
            continue
            
    #------------------
    invoiceTotal=0
    totalDiscount=0
    totalSpDiscount=0
    actual_total_tp=0
    for hRow in headRecords:
        invoiceTotal+=hRow[db.sm_invoice_head.id.count()]
        actual_total_tp+=hRow[db.sm_invoice_head.actual_total_tp.sum()]
        totalDiscount+=hRow[db.sm_invoice_head.discount.sum()]
        totalSpDiscount+=hRow[db.sm_invoice_head.sp_discount.sum()]
        #& (db.sm_invoice.quantity>0)
    records=qset((db.sm_invoice.cid==c_id) & (db.sm_invoice.depot_id==req_depot)&(db.sm_invoice_head.sl==db.sm_invoice.sl)).select(db.sm_invoice.level2_id,db.sm_invoice.item_id,db.sm_invoice.item_name.max(),db.sm_invoice.batch_id,db.sm_invoice.actual_tp,db.sm_invoice.price,db.sm_invoice.item_vat,db.sm_invoice.item_unit.max(),db.sm_invoice.quantity.sum(),db.sm_invoice.bonus_qty.sum(),orderby=db.sm_invoice.level2_id|db.sm_invoice.item_name|db.sm_invoice.batch_id|~db.sm_invoice.price,groupby=db.sm_invoice.level2_id|db.sm_invoice.item_id|db.sm_invoice.batch_id|db.sm_invoice.actual_tp|db.sm_invoice.price|db.sm_invoice.item_vat)      
    
    #-------------------------    
    if paymentMode=='':
        termsStr='ALL'
    else:
        termsStr=paymentMode
        
        if paymentMode=='CREDIT':
            if creditType=='':
                termsStr+='(ALL)'
            else:
                termsStr+='('+creditType+')'
    
    myString='(5.3) SYNOPSIS (Item List)With Batch-Before Delivery\n'
    myString+='SYNOPSIS (Before Delivery):,'+str(territory_id)+'\n'
    myString+='Market:,'+str(maxMarketID)+'|'+str(maxmarketName)+'\n'
    myString+='Delivery Person ID:,'+str(d_man_id)+'\n'
    myString+='Delivery Person Name:'+','+str(d_man_name)+'\n'
    myString+='Sales Term:,'+str(termsStr)+'\n'
    myString+='From Invoice:,'+str(search_from_sl)+'\n'
    myString+='To Invoice Range:'+','+str(search_to_sl)+'\n'
    myString+='From Date:,'+str(invoice_dateFrom)+'\n'
    myString+='To Date:,'+str(invoice_dateTo)+'\n'
    
    if territory_id!='':
        myString+=str(territory_id)+' Territory wise'+'\n'
    elif d_man_id!='':
        myString+='DP wise'+'\n'
        
    netTotal=0.0
    total_trade_price=0.0
    total_vat=0.0
    spDiscountTotal=0
    
    rowSl=0
    myString+='Sl.No,Item ID,Item Name,Batch No,Trade Price,Vat,Unit,Quantity,Bonus,Net Issue'+'\n'
    preArea=''
    for record in records:
        rowSl+=1        
        level2_id=record.sm_invoice.level2_id
        
        newArea=record.sm_invoice.level2_id
        if preArea!=newArea:            
            myString+=str(newArea)+'\n'    
            rowSl=0            
        preArea=newArea
        rowSl+=1
        
        
        item_id=record.sm_invoice.item_id
        item_name=str(record[db.sm_invoice.item_name.max()]).replace(',', ' ')        
        batch_id=record.sm_invoice.batch_id
        itemRate=record.sm_invoice.price
        itemQty=record[db.sm_invoice.quantity.sum()]
        actualTp=record.sm_invoice.actual_tp
        
        spDiscount=(actualTp-itemRate)*itemQty
        if spDiscount < 0:
            spDiscount=0
        spDiscountTotal+=spDiscount
        
        item_vat=record.sm_invoice.item_vat
        item_unit=record[db.sm_invoice.item_unit.max()]
        
        total_trade_price+=actualTp*itemQty
        
        total_vat+=record.sm_invoice.item_vat*itemQty
        
        bonus_qty=record[db.sm_invoice.bonus_qty.sum()]
        totalQty=itemQty+record[db.sm_invoice.bonus_qty.sum()]
        
        #------------------------        
        myString+=str(rowSl)+','+str(item_id)+','+str(item_name)+','+str(batch_id)+','+str(actualTp)+','+str(item_vat)+','+str(item_unit)+','+str(itemQty)+','+str(bonus_qty)+','+str(totalQty)+'\n'
    
    myString+='\n\nSummary,,,,,,,,,,,,,,,,,,,,\n'
    
    myString+='Total Trade Price:,'+str(round(total_trade_price,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='VAT:,'+str(round(total_vat,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Total Trade Concession Amount:,'+str(round(totalDiscount,2))+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Special Discount,'+str(round(spDiscountTotal,2))+',,,,,,,,,,,,,,,,,,,\n'
    netTotal=total_trade_price+total_vat-(totalDiscount+spDiscountTotal)
    myString+='Net Total:,'+str(round(netTotal,2))+',,,,,,,,,,,,,,,,,,,\n\n'
    
    inwordStr=num2word(str(round(netTotal,2)))
    
    myString+='Net Sales (Taka in Words):,'+str(inwordStr)+',,,,,,,,,,,,,,,,,,,\n'
    
    myString+='Total Invoice:,'+str(invoiceTotal)+',,,,,,,,,,,,,,,,,,,\n'
    myString+='Total Customer:,'+str(clientCount)+',,,,,,,,,,,,,,,,,,,\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_synopsisItemListBeforeDelivery.csv'   
    return str(myString)
    

#========================= Show Invoice invoice_item_list_synopsis after delivery store department
def invoice_item_list_synopsis_sd_after_del():
    c_id=session.cid
    req_depot=session.depot_id
    
    #--------------- Title
    response.title='5.1 Preview Synopsis SD With Batch After Delivery'
    
    #-------------    
    invoice_dateFrom=''
    invoice_dateTo=''
    
    territory_id=''
    territory_name=''    
    
    d_man_id=''
    d_man_name=''
    paymentMode=''
    search_from_sl=''
    search_to_sl=''
    creditType=''
    #----------------------
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.sl!=0)
    qset=qset(db.sm_invoice_head.depot_id==req_depot)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    
    #----------
    if (session.btn_filter_printm_s):
        if session.search_dt_from!='' and session.search_dt_to!='':
            qset=qset((db.sm_invoice_head.invoice_date>=session.search_dt_from)&(db.sm_invoice_head.invoice_date<=session.search_dt_to))
            invoice_dateFrom=session.search_dt_from
            invoice_dateTo=session.search_dt_to
            
        if session.search_from_sl>0 and session.search_to_sl>0:
            qset=qset((db.sm_invoice_head.sl>=session.search_from_sl)&(db.sm_invoice_head.sl<=session.search_to_sl))
            search_from_sl=session.search_from_sl
            search_to_sl=session.search_to_sl
            
        #------------
        if (session.search_type_printm_s=='REPID'):                
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.rep_id==searchValue)
            
        elif (session.search_type_printm_s=='ROUTEID'):
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.area_id==searchValue)
            
            territory_id=searchValue
            if territory_id!='':
                areaRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id) & (db.sm_level.is_leaf == '1')).select(db.sm_level.level_name,db.sm_level.level0,db.sm_level.level0_name,limitby=(0,1))
                if areaRow:
                    territory_name=areaRow[0].level_name
                    
        elif (session.search_type_printm_s=='CLIENTID'):
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.client_id==searchValue)
        
        elif (session.search_type_printm_s=='SHIPMENT'):
            searchValue=str(session.search_value_printm_s).strip()
            qset=qset(db.sm_invoice_head.shipment_no==searchValue)
            
        #----------
        if session.print_status=='Pending':
            qset=qset(db.sm_invoice_head.field2==0)
            
        #----------
        if session.paymentMode!='':
            paymentMode=session.paymentMode
            qset=qset(db.sm_invoice_head.payment_mode==paymentMode)
            
        #----------
        if session.creditType!='':
            qset=qset(db.sm_invoice_head.credit_note==session.creditType)
            creditType=session.creditType
            
        #----------
        if not(session.d_man_id_report=='' or session.d_man_id_report==None):
            searchValue=str(session.d_man_id_report).split('|')[0]
            qset=qset(db.sm_invoice_head.d_man_id==searchValue)
            
            d_man_id=searchValue
            dmanRecords=db((db.sm_delivery_man.cid==c_id)& (db.sm_delivery_man.depot_id==req_depot) & (db.sm_delivery_man.d_man_id==d_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
            if dmanRecords:
                d_man_name=dmanRecords[0].name
    
    
    headRecords1=qset.select(db.sm_invoice_head.client_id,db.sm_invoice_head.id.count(),db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),db.sm_invoice_head.return_sp_discount.sum(),groupby=db.sm_invoice_head.client_id)
    clientCount=len(headRecords1)
    #---------------------- maximum market Name
    maxMarketID=''
    maxmarketName=''
    maxCount=0
    rep_id=''
    rep_name=''
    area_id=''
    area_name=''
    headRecords2=qset.select(db.sm_invoice_head.market_id,db.sm_invoice_head.market_name.max(),db.sm_invoice_head.id.count(),db.sm_invoice_head.rep_id,db.sm_invoice_head.rep_name,db.sm_invoice_head.area_id,db.sm_invoice_head.area_name,groupby=db.sm_invoice_head.market_id)
    for headRec2 in headRecords2:
        market_id=headRec2.sm_invoice_head.market_id
        market_name=headRec2[db.sm_invoice_head.market_name.max()]
        market_count=headRec2[db.sm_invoice_head.id.count()]

        rep_id = headRec2.sm_invoice_head.rep_id
        rep_name = headRec2.sm_invoice_head.rep_name
        area_id = headRec2.sm_invoice_head.area_id
        area_name = headRec2.sm_invoice_head.area_name
        if market_count>maxCount:
            maxMarketID=market_id
            maxmarketName=market_name
            maxCount=market_count
        else:
            continue
    
    #------------------
    invoiceTotal=0    
    totalAmount=0
    vatTotal=0
    totalDiscount=0
    totalSpDiscount=0
    return_tp=0
    return_vat=0
    return_discount=0
    actual_total_tp=0
    return_sp_discount=0
    
    headRecords=qset.select(db.sm_invoice_head.depot_id,db.sm_invoice_head.id.count(),db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),db.sm_invoice_head.return_sp_discount.sum(),groupby=db.sm_invoice_head.depot_id)
    for hRow in headRecords:
        invoiceTotal+=hRow[db.sm_invoice_head.id.count()]
        #actual_total_tp+=hRow[db.sm_invoice_head.actual_total_tp.sum()]
        totalAmount+=hRow[db.sm_invoice_head.total_amount.sum()]
        #vatTotal+=hRow[db.sm_invoice_head.vat_total_amount.sum()]
        totalDiscount+=hRow[db.sm_invoice_head.discount.sum()]
        #totalSpDiscount+=hRow[db.sm_invoice_head.sp_discount.sum()]
        return_tp+=hRow[db.sm_invoice_head.return_tp.sum()]
        return_vat+=hRow[db.sm_invoice_head.return_vat.sum()]
        return_discount+=hRow[db.sm_invoice_head.return_discount.sum()]
        return_sp_discount+=hRow[db.sm_invoice_head.return_sp_discount.sum()]
        
    invRecords=qset((db.sm_invoice.cid==c_id) & (db.sm_invoice.depot_id==req_depot)&(db.sm_invoice_head.sl==db.sm_invoice.sl)).select(db.sm_invoice.item_id,db.sm_invoice.batch_id,db.sm_invoice.actual_tp,db.sm_invoice.price,db.sm_invoice.item_vat,db.sm_invoice.quantity.sum(),groupby=db.sm_invoice.item_id|db.sm_invoice.batch_id|db.sm_invoice.actual_tp|db.sm_invoice.price|db.sm_invoice.item_vat)      
    for invRow in invRecords:
        actualTp=invRow.sm_invoice.actual_tp
        itemRate=invRow.sm_invoice.price
        itemQty=invRow[db.sm_invoice.quantity.sum()]
        itemVat=invRow.sm_invoice.item_vat
        
        actual_total_tp+=actualTp*itemQty
        vatTotal+=itemVat*itemQty
        
        spDiscount=(actualTp-itemRate)*itemQty        
        totalSpDiscount+=spDiscount
    
    #----------
    records=qset((db.sm_invoice.cid==c_id) & (db.sm_invoice.depot_id==req_depot)&(db.sm_invoice_head.sl==db.sm_invoice.sl)).select(db.sm_invoice.item_id,db.sm_invoice.item_name.max(),db.sm_invoice.batch_id,db.sm_invoice.quantity.sum(),db.sm_invoice.bonus_qty.sum(),db.sm_invoice.return_qty.sum(),db.sm_invoice.return_bonus_qty.sum(),orderby=db.sm_invoice.item_name|db.sm_invoice.batch_id,groupby=db.sm_invoice.item_id|db.sm_invoice.batch_id)      
    
    #-------------------------
    return dict(records=records,maxMarketID=maxMarketID,maxmarketName=maxmarketName,paymentMode=paymentMode,creditType=creditType,search_from_sl=search_from_sl,search_to_sl=search_to_sl,territory_id=territory_id,territory_name=territory_name,invoice_dateFrom=invoice_dateFrom,invoice_dateTo=invoice_dateTo,d_man_id=d_man_id,d_man_name=d_man_name,rep_id=rep_id,rep_name=rep_name,area_id=area_id,area_name=area_name,clientCount=clientCount,invoiceTotal=invoiceTotal,actual_total_tp=actual_total_tp,return_sp_discount=return_sp_discount,totalAmount=totalAmount,vatTotal=vatTotal,totalDiscount=totalDiscount,totalSpDiscount=totalSpDiscount,return_tp=return_tp,return_vat=return_vat,return_discount=return_discount)

def invoice_item_list_synopsis_sd_after_del_download():
    c_id=session.cid
    req_depot=session.depot_id
    
    #-------------    
    invoice_dateFrom=''
    invoice_dateTo=''
    
    territory_id=''
    territory_name=''    
    
    d_man_id=''
    d_man_name=''
    paymentMode=''
    search_from_sl=''
    search_to_sl=''
    creditType=''
    #----------------------
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.sl!=0)
    qset=qset(db.sm_invoice_head.depot_id==req_depot)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    
    #----------
    if (session.btn_filter_printm_s):
        if session.search_dt_from!='' and session.search_dt_to!='':
            qset=qset((db.sm_invoice_head.invoice_date>=session.search_dt_from)&(db.sm_invoice_head.invoice_date<=session.search_dt_to))
            invoice_dateFrom=session.search_dt_from
            invoice_dateTo=session.search_dt_to
            
        if session.search_from_sl>0 and session.search_to_sl>0:
            qset=qset((db.sm_invoice_head.sl>=session.search_from_sl)&(db.sm_invoice_head.sl<=session.search_to_sl))
            search_from_sl=session.search_from_sl
            search_to_sl=session.search_to_sl
            
        #------------
        if (session.search_type_printm_s=='REPID'):                
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.rep_id==searchValue)
            
        elif (session.search_type_printm_s=='ROUTEID'):
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.area_id==searchValue)
            
            territory_id=searchValue
            if territory_id!='':
                areaRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id) & (db.sm_level.is_leaf == '1')).select(db.sm_level.level_name,db.sm_level.level0,db.sm_level.level0_name,limitby=(0,1))
                if areaRow:
                    territory_name=areaRow[0].level_name
                    
        elif (session.search_type_printm_s=='CLIENTID'):
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.client_id==searchValue)
        
        elif (session.search_type_printm_s=='SHIPMENT'):
            searchValue=str(session.search_value_printm_s).strip()
            qset=qset(db.sm_invoice_head.shipment_no==searchValue)
            
        #----------
        if session.print_status=='Pending':
            qset=qset(db.sm_invoice_head.field2==0)
            
        #----------
        if session.paymentMode!='':
            paymentMode=session.paymentMode
            qset=qset(db.sm_invoice_head.payment_mode==paymentMode)
            
        #----------
        if session.creditType!='':
            qset=qset(db.sm_invoice_head.credit_note==session.creditType)
            creditType=session.creditType
            
        #----------
        if not(session.d_man_id_report=='' or session.d_man_id_report==None):
            searchValue=str(session.d_man_id_report).split('|')[0]
            qset=qset(db.sm_invoice_head.d_man_id==searchValue)
            
            d_man_id=searchValue
            dmanRecords=db((db.sm_delivery_man.cid==c_id)& (db.sm_delivery_man.depot_id==req_depot) & (db.sm_delivery_man.d_man_id==d_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
            if dmanRecords:
                d_man_name=dmanRecords[0].name
    
    
    headRecords1=qset.select(db.sm_invoice_head.client_id,db.sm_invoice_head.id.count(),db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),db.sm_invoice_head.return_sp_discount.sum(),groupby=db.sm_invoice_head.client_id)
    clientCount=len(headRecords1)
    #---------------------- maximum market Name
    maxMarketID=''
    maxmarketName=''
    maxCount=0
    rep_id = ''
    rep_name = ''
    area_id = ''
    area_name = ''
    headRecords2=qset.select(db.sm_invoice_head.market_id,db.sm_invoice_head.market_name.max(),db.sm_invoice_head.id.count(),db.sm_invoice_head.rep_id,db.sm_invoice_head.rep_name,db.sm_invoice_head.area_id,db.sm_invoice_head.area_name,groupby=db.sm_invoice_head.market_id)
    for headRec2 in headRecords2:
        market_id=headRec2.sm_invoice_head.market_id
        market_name=headRec2[db.sm_invoice_head.market_name.max()]
        market_count=headRec2[db.sm_invoice_head.id.count()]

        rep_id = headRec2.sm_invoice_head.rep_id
        rep_name = headRec2.sm_invoice_head.rep_name
        area_id = headRec2.sm_invoice_head.area_id
        area_name = headRec2.sm_invoice_head.area_name

        if market_count>maxCount:
            maxMarketID=market_id
            maxmarketName=market_name
            maxCount=market_count
        else:
            continue
    
    #------------------
    invoiceTotal=0    
    totalAmount=0
    vatTotal=0
    totalDiscount=0
    totalSpDiscount=0
    return_tp=0
    return_vat=0
    return_discount=0
    actual_total_tp=0
    return_sp_discount=0
    
    headRecords=qset.select(db.sm_invoice_head.depot_id,db.sm_invoice_head.id.count(),db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),db.sm_invoice_head.return_sp_discount.sum(),groupby=db.sm_invoice_head.depot_id)
    for hRow in headRecords:
        invoiceTotal+=hRow[db.sm_invoice_head.id.count()]
        #actual_total_tp+=hRow[db.sm_invoice_head.actual_total_tp.sum()]
        totalAmount+=hRow[db.sm_invoice_head.total_amount.sum()]
        #vatTotal+=hRow[db.sm_invoice_head.vat_total_amount.sum()]
        totalDiscount+=hRow[db.sm_invoice_head.discount.sum()]
        #totalSpDiscount+=hRow[db.sm_invoice_head.sp_discount.sum()]
        return_tp+=hRow[db.sm_invoice_head.return_tp.sum()]
        return_vat+=hRow[db.sm_invoice_head.return_vat.sum()]
        return_discount+=hRow[db.sm_invoice_head.return_discount.sum()]
        return_sp_discount+=hRow[db.sm_invoice_head.return_sp_discount.sum()]
        
    invRecords=qset((db.sm_invoice.cid==c_id) & (db.sm_invoice.depot_id==req_depot)&(db.sm_invoice_head.sl==db.sm_invoice.sl)).select(db.sm_invoice.item_id,db.sm_invoice.batch_id,db.sm_invoice.actual_tp,db.sm_invoice.price,db.sm_invoice.item_vat,db.sm_invoice.quantity.sum(),groupby=db.sm_invoice.item_id|db.sm_invoice.batch_id|db.sm_invoice.actual_tp|db.sm_invoice.price|db.sm_invoice.item_vat)      
    for invRow in invRecords:
        actualTp=invRow.sm_invoice.actual_tp
        itemRate=invRow.sm_invoice.price
        itemQty=invRow[db.sm_invoice.quantity.sum()]
        itemVat=invRow.sm_invoice.item_vat
        
        actual_total_tp+=actualTp*itemQty
        vatTotal+=itemVat*itemQty
        
        spDiscount=(actualTp-itemRate)*itemQty        
        totalSpDiscount+=spDiscount
    
    #----------
    records=qset((db.sm_invoice.cid==c_id) & (db.sm_invoice.depot_id==req_depot)&(db.sm_invoice_head.sl==db.sm_invoice.sl)).select(db.sm_invoice.item_id,db.sm_invoice.item_name.max(),db.sm_invoice.batch_id,db.sm_invoice.quantity.sum(),db.sm_invoice.bonus_qty.sum(),db.sm_invoice.return_qty.sum(),db.sm_invoice.return_bonus_qty.sum(),orderby=db.sm_invoice.item_name|db.sm_invoice.batch_id,groupby=db.sm_invoice.item_id|db.sm_invoice.batch_id)      
    
    
    #-------------------------
    if paymentMode=='':
        termsStr='ALL'
    else:
        termsStr=paymentMode
        
        if paymentMode=='CREDIT':
            if creditType=='':
                termsStr+='(ALL)'
            else:
                termsStr+='('+creditType+')'
    
    
    myString='(5.1) SYNOPSIS Product Report(Store Dept)With Batch-After Delivery\n'
    myString+='SYNOPSIS (After Delivery):'+'\n'
    myString+='Market:,'+str(maxMarketID)+'|'+str(maxmarketName)+'\n'
    myString += 'Mso Name:,' + str(rep_name) + '\n' #+ str(rep_id) + '|'
    myString += 'Territory:,' + str(area_name) + '\n' #+ str(area_id) + '|'
    myString+='Delivery Person ID:,'+str(d_man_id)+'\n'
    myString+='Delivery Person Name:'+','+str(d_man_name)+'\n'
    myString+='Sales Term:,'+str(termsStr)+'\n'
    myString+='From Invoice:,'+str(search_from_sl)+'\n'
    myString+='To Invoice Range:'+','+str(search_to_sl)+'\n'
    myString+='From Date:,'+str(invoice_dateFrom)+'\n'
    myString+='To Date:,'+str(invoice_dateTo)+'\n'
    
    rowSl=0
    myString+='SL,Item ID,Item Name,Batch,Invoice-Qnty,Invoice-BonusQnty,Return-Qnty,Return-BonusQnty,Net Issue-Sold Qnty,Net Issue-Bonus Qnty'+'\n'
    for record in records:
        rowSl+=1
        
        item_id=record.sm_invoice.item_id
        item_name=str(record[db.sm_invoice.item_name.max()]).replace(',', ' ')        
        batch_id=record.sm_invoice.batch_id        
        itemQty=record[db.sm_invoice.quantity.sum()]
        bonus_qty=record[db.sm_invoice.bonus_qty.sum()]
        return_qty=record[db.sm_invoice.return_qty.sum()]
        return_bonus_qty=record[db.sm_invoice.return_bonus_qty.sum()]
        
        soldQty=record[db.sm_invoice.quantity.sum()]-record[db.sm_invoice.return_qty.sum()]
        bonusQty=record[db.sm_invoice.bonus_qty.sum()]-record[db.sm_invoice.return_bonus_qty.sum()]
        
        #------------------------        
        myString+=str(rowSl)+','+str(item_id)+','+str(item_name)+','+str(batch_id)+','+str(itemQty)+','+str(bonus_qty)+','+str(return_qty)+','+str(return_bonus_qty)+','+str(soldQty)+','+str(bonusQty)+'\n'
    
    myString+='\n\nSummary\n'
    
    myString+='DOCUMENT'+'\n'
    myString+='Invoice:,'+str(round(invoiceTotal,2))+'\n'
    myString+='Credit Note:,'+'\n'
    myString+='Debit Note:,'+'\n'
    myString+='Customer:,'+str(round(clientCount,2))+'\n\n'
    
    myString+=',INVOICE,RETURN,NET'+'\n'
    myString+='Sub Total(TP):,'+str(round(actual_total_tp,2))+',-'+str(round(return_tp+return_sp_discount,2))+','+str(round(actual_total_tp-(return_tp+return_sp_discount),2))+'\n'
    myString+='VAT:,'+str(round(vatTotal,2))+',-'+str(round(return_vat,2))+','+str(round(vatTotal-return_vat,2))+'\n'
    myString+='Discount:,'+str(round(totalDiscount,2))+',-'+str(round(return_discount,2))+','+str(round(totalDiscount-return_discount,2))+'\n'
    myString+='Special Discount:,'+str(round(totalSpDiscount,2))+',-'+str(round(return_sp_discount,2))+','+str(round(totalSpDiscount-return_sp_discount,2))+'\n'
    
    invTotal=(actual_total_tp+vatTotal-(totalDiscount+totalSpDiscount))
    totalReturn=return_tp+return_vat-return_discount
    netSale=invTotal-totalReturn
    
    myString+='Total:,'+str(round(invTotal,2))+',-'+str(round(totalReturn,2))+','+str(round(netSale,2))+'\n'
        
    inwordStr=num2word(str(round(netSale,2)))
    
    myString+='Net Sales (Taka in Words):,'+str(inwordStr)+',,,,,,,,,,,,,,,,,,,\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_synopsisProductRptSDAfterDelivery.csv'   
    return str(myString)
    

#========================= Show Invoice invoice_item_list_synopsis after delivery account department
def invoice_item_list_synopsis_ad_after_del():
    c_id=session.cid
    req_depot=session.depot_id
    
    #--------------- Title
    response.title='5.1 Preview Synopsis AD After Delivery'
    
    #-------------    
    invoice_dateFrom=''
    invoice_dateTo=''
    
    territory_id=''
    territory_name=''    
    
    d_man_id=''
    d_man_name=''
    paymentMode=''
    search_from_sl=''
    search_to_sl=''
    creditType=''
    
    #----------------------
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.sl!=0)
    qset=qset(db.sm_invoice_head.depot_id==req_depot)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    
    #----------
    if (session.btn_filter_printm_s):
        if session.search_dt_from!='' and session.search_dt_to!='':
            qset=qset((db.sm_invoice_head.invoice_date>=session.search_dt_from)&(db.sm_invoice_head.invoice_date<=session.search_dt_to))
            invoice_dateFrom=session.search_dt_from
            invoice_dateTo=session.search_dt_to
            
        if session.search_from_sl>0 and session.search_to_sl>0:
            qset=qset((db.sm_invoice_head.sl>=session.search_from_sl)&(db.sm_invoice_head.sl<=session.search_to_sl))
            search_from_sl=session.search_from_sl
            search_to_sl=session.search_to_sl
            
        #------------
        if (session.search_type_printm_s=='REPID'):                
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.rep_id==searchValue)
            
        elif (session.search_type_printm_s=='ROUTEID'):
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.area_id==searchValue)
            
            territory_id=searchValue
            if territory_id!='':
                areaRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id) & (db.sm_level.is_leaf == '1')).select(db.sm_level.level_name,db.sm_level.level0,db.sm_level.level0_name,limitby=(0,1))
                if areaRow:
                    territory_name=areaRow[0].level_name
                    
        elif (session.search_type_printm_s=='CLIENTID'):
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.client_id==searchValue)
        
        elif (session.search_type_printm_s=='SHIPMENT'):
            searchValue=str(session.search_value_printm_s).strip()
            qset=qset(db.sm_invoice_head.shipment_no==searchValue)
            
        #----------
        if session.print_status=='Pending':
            qset=qset(db.sm_invoice_head.field2==0)
            
        #----------
        if session.paymentMode!='':
            paymentMode=session.paymentMode
            qset=qset(db.sm_invoice_head.payment_mode==paymentMode)
            
        #----------
        if session.creditType!='':
            qset=qset(db.sm_invoice_head.credit_note==session.creditType)
            creditType=session.creditType
            
        #----------
        if not(session.d_man_id_report=='' or session.d_man_id_report==None):
            searchValue=str(session.d_man_id_report).split('|')[0]
            qset=qset(db.sm_invoice_head.d_man_id==searchValue)
            
            d_man_id=searchValue
            dmanRecords=db((db.sm_delivery_man.cid==c_id)& (db.sm_delivery_man.depot_id==req_depot) & (db.sm_delivery_man.d_man_id==d_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
            if dmanRecords:
                d_man_name=dmanRecords[0].name
    
    headRecords=qset.select(db.sm_invoice_head.client_id,db.sm_invoice_head.id.count(),db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),db.sm_invoice_head.return_sp_discount.sum(),groupby=db.sm_invoice_head.client_id)
    clientCount=len(headRecords)
    #---------------------- maximum market Name
    maxMarketID=''
    maxmarketName=''
    maxCount=0
    headRecords2=qset.select(db.sm_invoice_head.market_id,db.sm_invoice_head.market_name.max(),db.sm_invoice_head.id.count(),groupby=db.sm_invoice_head.market_id)
    for headRec2 in headRecords2:
        market_id=headRec2.sm_invoice_head.market_id
        market_name=headRec2[db.sm_invoice_head.market_name.max()]
        market_count=headRec2[db.sm_invoice_head.id.count()]        
        if market_count>maxCount:
            maxMarketID=market_id
            maxmarketName=market_name
            maxCount=market_count
        else:
            continue
            
    #------------------
    invoiceTotal=0    
        
    for hRow in headRecords:
        invoiceTotal+=hRow[db.sm_invoice_head.id.count()]
        
    records=qset.select(db.sm_invoice_head.ALL,orderby=db.sm_invoice_head.sl)
    
    #-------------------------
    return dict(records=records,maxMarketID=maxMarketID,maxmarketName=maxmarketName,paymentMode=paymentMode,creditType=creditType,search_from_sl=search_from_sl,search_to_sl=search_to_sl,territory_id=territory_id,territory_name=territory_name,invoice_dateFrom=invoice_dateFrom,invoice_dateTo=invoice_dateTo,d_man_id=d_man_id,d_man_name=d_man_name,clientCount=clientCount,invoiceTotal=invoiceTotal)

def invoice_item_list_synopsis_ad_after_del_download():
    c_id=session.cid
    req_depot=session.depot_id
    
    #--------------- Title
    response.title='Preview Synopsis AD After Delivery'
    
    #-------------    
    invoice_dateFrom=''
    invoice_dateTo=''
    
    territory_id=''
    territory_name=''    
    
    d_man_id=''
    d_man_name=''
    paymentMode=''
    search_from_sl=''
    search_to_sl=''
    creditType=''
    
    #----------------------
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.sl!=0)
    qset=qset(db.sm_invoice_head.depot_id==req_depot)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    
    #----------
    if (session.btn_filter_printm_s):
        if session.search_dt_from!='' and session.search_dt_to!='':
            qset=qset((db.sm_invoice_head.invoice_date>=session.search_dt_from)&(db.sm_invoice_head.invoice_date<=session.search_dt_to))
            invoice_dateFrom=session.search_dt_from
            invoice_dateTo=session.search_dt_to
            
        if session.search_from_sl>0 and session.search_to_sl>0:
            qset=qset((db.sm_invoice_head.sl>=session.search_from_sl)&(db.sm_invoice_head.sl<=session.search_to_sl))
            search_from_sl=session.search_from_sl
            search_to_sl=session.search_to_sl
            
        #------------
        if (session.search_type_printm_s=='REPID'):                
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.rep_id==searchValue)
            
        elif (session.search_type_printm_s=='ROUTEID'):
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.area_id==searchValue)
            
            territory_id=searchValue
            if territory_id!='':
                areaRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id) & (db.sm_level.is_leaf == '1')).select(db.sm_level.level_name,db.sm_level.level0,db.sm_level.level0_name,limitby=(0,1))
                if areaRow:
                    territory_name=areaRow[0].level_name
                    
        elif (session.search_type_printm_s=='CLIENTID'):
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.client_id==searchValue)
        
        elif (session.search_type_printm_s=='SHIPMENT'):
            searchValue=str(session.search_value_printm_s).strip()
            qset=qset(db.sm_invoice_head.shipment_no==searchValue)
            
        #----------
        if session.print_status=='Pending':
            qset=qset(db.sm_invoice_head.field2==0)
            
        #----------
        if session.paymentMode!='':
            paymentMode=session.paymentMode
            qset=qset(db.sm_invoice_head.payment_mode==paymentMode)
            
        #----------
        if session.creditType!='':
            qset=qset(db.sm_invoice_head.credit_note==session.creditType)
            creditType=session.creditType
            
        #----------
        if not(session.d_man_id_report=='' or session.d_man_id_report==None):
            searchValue=str(session.d_man_id_report).split('|')[0]
            qset=qset(db.sm_invoice_head.d_man_id==searchValue)
            
            d_man_id=searchValue
            dmanRecords=db((db.sm_delivery_man.cid==c_id)& (db.sm_delivery_man.depot_id==req_depot) & (db.sm_delivery_man.d_man_id==d_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
            if dmanRecords:
                d_man_name=dmanRecords[0].name
    
    headRecords=qset.select(db.sm_invoice_head.client_id,db.sm_invoice_head.id.count(),db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),db.sm_invoice_head.return_sp_discount.sum(),groupby=db.sm_invoice_head.client_id)
    clientCount=len(headRecords)
    #---------------------- maximum market Name
    maxMarketID=''
    maxmarketName=''
    maxCount=0
    headRecords2=qset.select(db.sm_invoice_head.market_id,db.sm_invoice_head.market_name.max(),db.sm_invoice_head.id.count(),groupby=db.sm_invoice_head.market_id)
    for headRec2 in headRecords2:
        market_id=headRec2.sm_invoice_head.market_id
        market_name=headRec2[db.sm_invoice_head.market_name.max()]
        market_count=headRec2[db.sm_invoice_head.id.count()]        
        if market_count>maxCount:
            maxMarketID=market_id
            maxmarketName=market_name
            maxCount=market_count
        else:
            continue
    
    #------------------
    invoiceTotal=0    
        
    for hRow in headRecords:
        invoiceTotal+=hRow[db.sm_invoice_head.id.count()]
        
    records=qset.select(db.sm_invoice_head.ALL,orderby=db.sm_invoice_head.sl)    
    #-------------------------
    if paymentMode=='':
        termsStr='ALL'
    else:
        termsStr=paymentMode
        
        if paymentMode=='CREDIT':
            if creditType=='':
                termsStr+='(ALL)'
            else:
                termsStr+='('+creditType+')'
    
    
    myString='(5.1) SYNOPSIS Transaction Report(Acc Dept)-After Delivery\n'
    myString+='SYNOPSIS (After Delivery):'+'\n'
    myString+='Market:,'+str(maxMarketID)+'|'+str(maxmarketName)+'\n'
    myString+='Delivery Person ID:,'+str(d_man_id)+'\n'
    myString+='Delivery Person Name:'+','+str(d_man_name)+'\n'
    myString+='Sales Term:,'+str(termsStr)+'\n'
    myString+='From Invoice:,'+str(search_from_sl)+'\n'
    myString+='To Invoice Range:'+','+str(search_to_sl)+'\n'
    myString+='From Date:,'+str(invoice_dateFrom)+'\n'
    myString+='To Date:,'+str(invoice_dateTo)+'\n'
    
    total_amount=0
    
    myString+='Cust ID,Customer Name,Terms,Invoice,Date,Tp,VAT,Disc,SpDisc,Net Sale'+'\n'
    for record in records:        
        client_id=record.client_id
        client_name=str(record.client_name).replace(',', ' ')        
        payment_mode=record.payment_mode
        invSl=str(session.prefix_invoice)+'INV'+str(record.depot_id)+'-'+str(record.sl)
        invoice_date=record.invoice_date
        
        tpAmt=record.actual_total_tp-(record.return_tp+record.return_sp_discount)
        vatAmt=(record.vat_total_amount-record.return_vat)
        discAmt=(record.discount-record.return_discount)
        spDiscAmt=(record.sp_discount-record.return_sp_discount)
        totalAmt=tpAmt+vatAmt-(discAmt+spDiscAmt)
        
        total_amount+=totalAmt
        
        #------------------------        
        myString+=str(client_id)+','+str(client_name)+','+str(payment_mode)+','+str(invSl)+','+str(invoice_date)+','+str(tpAmt)+','+str(vatAmt)+','+str(discAmt)+','+str(spDiscAmt)+','+str(totalAmt)+'\n'
    
    
    myString+=str(invoiceTotal)+' Invoice(s),,,,,,,,Total:,'+str(round(total_amount,2))+'\n'
    
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_synopsisTransactionRptADAfterDelivery.csv'   
    return str(myString)
    
#========================= Show Invoice invoice_item_list_synopsis after delivery account department with Return Details
def invoice_item_list_synopsis_ad_after_del_retDet():
    c_id=session.cid
    req_depot=session.depot_id
    
    #--------------- Title
    response.title='5.1.1 Preview Synopsis AD After Delivery With Return Details'
    
    #-------------    
    invoice_dateFrom=''
    invoice_dateTo=''
    
    territory_id=''
    territory_name=''    
    
    d_man_id=''
    d_man_name=''
    paymentMode=''
    search_from_sl=''
    search_to_sl=''
    creditType=''
    
    #----------------------
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.sl!=0)
    qset=qset(db.sm_invoice_head.depot_id==req_depot)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    
    #----------
    if (session.btn_filter_printm_s):
        if session.search_dt_from!='' and session.search_dt_to!='':
            qset=qset((db.sm_invoice_head.invoice_date>=session.search_dt_from)&(db.sm_invoice_head.invoice_date<=session.search_dt_to))
            invoice_dateFrom=session.search_dt_from
            invoice_dateTo=session.search_dt_to
            
        if session.search_from_sl>0 and session.search_to_sl>0:
            qset=qset((db.sm_invoice_head.sl>=session.search_from_sl)&(db.sm_invoice_head.sl<=session.search_to_sl))
            search_from_sl=session.search_from_sl
            search_to_sl=session.search_to_sl
            
        #------------
        if (session.search_type_printm_s=='REPID'):                
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.rep_id==searchValue)
            
        elif (session.search_type_printm_s=='ROUTEID'):
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.area_id==searchValue)
            
            territory_id=searchValue
            if territory_id!='':
                areaRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id) & (db.sm_level.is_leaf == '1')).select(db.sm_level.level_name,db.sm_level.level0,db.sm_level.level0_name,limitby=(0,1))
                if areaRow:
                    territory_name=areaRow[0].level_name
                    
        elif (session.search_type_printm_s=='CLIENTID'):
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.client_id==searchValue)
        
        elif (session.search_type_printm_s=='SHIPMENT'):
            searchValue=str(session.search_value_printm_s).strip()
            qset=qset(db.sm_invoice_head.shipment_no==searchValue)
            
        #----------
        if session.print_status=='Pending':
            qset=qset(db.sm_invoice_head.field2==0)
            
        #----------
        if session.paymentMode!='':
            paymentMode=session.paymentMode
            qset=qset(db.sm_invoice_head.payment_mode==paymentMode)
            
        #----------
        if session.creditType!='':
            qset=qset(db.sm_invoice_head.credit_note==session.creditType)
            creditType=session.creditType
            
        #----------
        if not(session.d_man_id_report=='' or session.d_man_id_report==None):
            searchValue=str(session.d_man_id_report).split('|')[0]
            qset=qset(db.sm_invoice_head.d_man_id==searchValue)
            
            d_man_id=searchValue
            dmanRecords=db((db.sm_delivery_man.cid==c_id)& (db.sm_delivery_man.depot_id==req_depot) & (db.sm_delivery_man.d_man_id==d_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
            if dmanRecords:
                d_man_name=dmanRecords[0].name
    
    headRecords=qset.select(db.sm_invoice_head.client_id,db.sm_invoice_head.id.count(),db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),db.sm_invoice_head.return_sp_discount.sum(),groupby=db.sm_invoice_head.client_id)
    clientCount=len(headRecords)
    #---------------------- maximum market Name
    maxMarketID=''
    maxmarketName=''
    maxCount=0
    headRecords2=qset.select(db.sm_invoice_head.market_id,db.sm_invoice_head.market_name.max(),db.sm_invoice_head.id.count(),groupby=db.sm_invoice_head.market_id)
    for headRec2 in headRecords2:
        market_id=headRec2.sm_invoice_head.market_id
        market_name=headRec2[db.sm_invoice_head.market_name.max()]
        market_count=headRec2[db.sm_invoice_head.id.count()]        
        if market_count>maxCount:
            maxMarketID=market_id
            maxmarketName=market_name
            maxCount=market_count
        else:
            continue
            
    #------------------
    invoiceTotal=0    
        
    for hRow in headRecords:
        invoiceTotal+=hRow[db.sm_invoice_head.id.count()]
    
    records=qset.select(db.sm_invoice_head.ALL,orderby=db.sm_invoice_head.sl)
    
    
    qset=qset(db.sm_return_head.cid==c_id)    
    qset=qset(db.sm_return_head.depot_id==req_depot)
    qset=qset(db.sm_return_head.status=='Returned')
    qset=qset(db.sm_invoice_head.sl==db.sm_return_head.invoice_sl)    
    retRecords=qset.select(db.sm_return_head.depot_id,db.sm_return_head.sl,db.sm_return_head.return_date,db.sm_return_head.invoice_sl,db.sm_return_head.ret_actual_total_tp,db.sm_return_head.total_amount,db.sm_return_head.vat_total_amount,db.sm_return_head.discount,db.sm_return_head.sp_discount,orderby=db.sm_return_head.invoice_sl)
    returnList=retRecords.as_list()
    
    #-------------------------
    return dict(records=records,returnList=returnList,maxMarketID=maxMarketID,maxmarketName=maxmarketName,paymentMode=paymentMode,creditType=creditType,search_from_sl=search_from_sl,search_to_sl=search_to_sl,territory_id=territory_id,territory_name=territory_name,invoice_dateFrom=invoice_dateFrom,invoice_dateTo=invoice_dateTo,d_man_id=d_man_id,d_man_name=d_man_name,clientCount=clientCount,invoiceTotal=invoiceTotal)

def invoice_item_list_synopsis_ad_after_del_retDet_download():
    c_id=session.cid
    req_depot=session.depot_id
    
    #--------------- Title
    response.title='Preview Synopsis AD After Delivery With Return Details'
    
    #-------------    
    invoice_dateFrom=''
    invoice_dateTo=''
    
    territory_id=''
    territory_name=''    
    
    d_man_id=''
    d_man_name=''
    paymentMode=''
    search_from_sl=''
    search_to_sl=''
    creditType=''
    
    #----------------------
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.sl!=0)
    qset=qset(db.sm_invoice_head.depot_id==req_depot)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    
    #----------
    if (session.btn_filter_printm_s):
        if session.search_dt_from!='' and session.search_dt_to!='':
            qset=qset((db.sm_invoice_head.invoice_date>=session.search_dt_from)&(db.sm_invoice_head.invoice_date<=session.search_dt_to))
            invoice_dateFrom=session.search_dt_from
            invoice_dateTo=session.search_dt_to
            
        if session.search_from_sl>0 and session.search_to_sl>0:
            qset=qset((db.sm_invoice_head.sl>=session.search_from_sl)&(db.sm_invoice_head.sl<=session.search_to_sl))
            search_from_sl=session.search_from_sl
            search_to_sl=session.search_to_sl
            
        #------------
        if (session.search_type_printm_s=='REPID'):                
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.rep_id==searchValue)
            
        elif (session.search_type_printm_s=='ROUTEID'):
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.area_id==searchValue)
            
            territory_id=searchValue
            if territory_id!='':
                areaRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id) & (db.sm_level.is_leaf == '1')).select(db.sm_level.level_name,db.sm_level.level0,db.sm_level.level0_name,limitby=(0,1))
                if areaRow:
                    territory_name=areaRow[0].level_name
                    
        elif (session.search_type_printm_s=='CLIENTID'):
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.client_id==searchValue)
        
        elif (session.search_type_printm_s=='SHIPMENT'):
            searchValue=str(session.search_value_printm_s).strip()
            qset=qset(db.sm_invoice_head.shipment_no==searchValue)
            
        #----------
        if session.print_status=='Pending':
            qset=qset(db.sm_invoice_head.field2==0)
            
        #----------
        if session.paymentMode!='':
            paymentMode=session.paymentMode
            qset=qset(db.sm_invoice_head.payment_mode==paymentMode)
            
        #----------
        if session.creditType!='':
            qset=qset(db.sm_invoice_head.credit_note==session.creditType)
            creditType=session.creditType
            
        #----------
        if not(session.d_man_id_report=='' or session.d_man_id_report==None):
            searchValue=str(session.d_man_id_report).split('|')[0]
            qset=qset(db.sm_invoice_head.d_man_id==searchValue)
            
            d_man_id=searchValue
            dmanRecords=db((db.sm_delivery_man.cid==c_id)& (db.sm_delivery_man.depot_id==req_depot) & (db.sm_delivery_man.d_man_id==d_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
            if dmanRecords:
                d_man_name=dmanRecords[0].name
    
    headRecords=qset.select(db.sm_invoice_head.client_id,db.sm_invoice_head.id.count(),db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),db.sm_invoice_head.return_sp_discount.sum(),groupby=db.sm_invoice_head.client_id)
    clientCount=len(headRecords)
    #---------------------- maximum market Name
    maxMarketID=''
    maxmarketName=''
    maxCount=0
    headRecords2=qset.select(db.sm_invoice_head.market_id,db.sm_invoice_head.market_name.max(),db.sm_invoice_head.id.count(),groupby=db.sm_invoice_head.market_id)
    for headRec2 in headRecords2:
        market_id=headRec2.sm_invoice_head.market_id
        market_name=headRec2[db.sm_invoice_head.market_name.max()]
        market_count=headRec2[db.sm_invoice_head.id.count()]        
        if market_count>maxCount:
            maxMarketID=market_id
            maxmarketName=market_name
            maxCount=market_count
        else:
            continue
    
    #------------------
    invoiceTotal=0    
        
    for hRow in headRecords:
        invoiceTotal+=hRow[db.sm_invoice_head.id.count()]
        
    records=qset.select(db.sm_invoice_head.ALL,orderby=db.sm_invoice_head.sl)
    
    qset=qset(db.sm_return_head.cid==c_id)    
    qset=qset(db.sm_return_head.depot_id==req_depot)
    qset=qset(db.sm_return_head.status=='Returned')
    qset=qset(db.sm_invoice_head.sl==db.sm_return_head.invoice_sl)    
    retRecords=qset.select(db.sm_return_head.depot_id,db.sm_return_head.sl,db.sm_return_head.return_date,db.sm_return_head.invoice_sl,db.sm_return_head.ret_actual_total_tp,db.sm_return_head.total_amount,db.sm_return_head.vat_total_amount,db.sm_return_head.discount,db.sm_return_head.sp_discount,orderby=db.sm_return_head.invoice_sl)
    returnList=retRecords.as_list()
    
    #-------------------------
    if paymentMode=='':
        termsStr='ALL'
    else:
        termsStr=paymentMode
        
        if paymentMode=='CREDIT':
            if creditType=='':
                termsStr+='(ALL)'
            else:
                termsStr+='('+creditType+')'
    
    
    myString='(5.1.1) SYNOPSIS Transaction Report(Acc Dept)-After Delivery With Return Details\n'
    myString+='SYNOPSIS (After Delivery):'+'\n'
    myString+='Market:,'+str(maxMarketID)+'|'+str(maxmarketName)+'\n'
    myString+='Delivery Person ID:,'+str(d_man_id)+'\n'
    myString+='Delivery Person Name:'+','+str(d_man_name)+'\n'
    myString+='Sales Term:,'+str(termsStr)+'\n'
    myString+='From Invoice:,'+str(search_from_sl)+'\n'
    myString+='To Invoice Range:'+','+str(search_to_sl)+'\n'
    myString+='From Date:,'+str(invoice_dateFrom)+'\n'
    myString+='To Date:,'+str(invoice_dateTo)+'\n'
    
    total_amount=0
    
    myString+='Cust ID,Customer Name,Terms,Shipment No,Date,Ref,Tp,VAT,Disc,SpDisc,Net Sale'+'\n'
    for record in records:        
        client_id=record.client_id
        client_name=str(record.client_name).replace(',', ' ')        
        payment_mode=record.payment_mode
        invSl=str(session.prefix_invoice)+'INV'+str(record.depot_id)+'-'+str(record.sl)
        invoice_date=record.invoice_date
        shipment_no=record.shipment_no
        
        actual_total_tp=record.actual_total_tp
        vat_total_amount=record.vat_total_amount
        discount=record.discount
        sp_discount=record.sp_discount
        
        tpAmt=record.actual_total_tp-(record.return_tp+record.return_sp_discount)
        vatAmt=(record.vat_total_amount-record.return_vat)
        discAmt=(record.discount-record.return_discount)
        spDiscAmt=(record.sp_discount-record.return_sp_discount)
        totalAmt=tpAmt+vatAmt-(discAmt+spDiscAmt)
        
        total_amount+=totalAmt
        
        #------------------------        
        myString+=str(client_id)+','+str(client_name)+','+str(payment_mode)+','+str(shipment_no)+','+str(invoice_date)+','+str(invSl)+','+str(actual_total_tp)+','+str(vat_total_amount)+','+str(discount)+','+str(sp_discount)+','+str(totalAmt)+'\n'
        
        for j in range(len(returnList)):
            retDict=returnList[j]
            ret_invoice_sl=retDict['invoice_sl']
            
            if record.sl==ret_invoice_sl:               
               return_date=retDict['return_date']
               retSl=str(session.prefix_invoice)+'RET'+str(retDict['depot_id'])+'-'+str(retDict['sl'])
               ret_actual_total_tp=retDict['ret_actual_total_tp']
               ret_vat_total_amount=retDict['vat_total_amount']
               ret_discount=retDict['discount']
               ret_sp_discount=retDict['sp_discount']
               
               #------------------------        
               myString+=',,,,'+str(return_date)+','+str(retSl)+',('+str(ret_actual_total_tp)+'),('+str(ret_vat_total_amount)+'),('+str(ret_discount)+'),('+str(ret_sp_discount)+'),\n'
                
    myString+=str(invoiceTotal)+' Invoice(s),,,,,,,,,Total:,'+str(round(total_amount,2))+'\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_synopsisTransactionRptADAfterDelivery_ReturnDet.csv'   
    return str(myString)
    

#========================= Show Invoice invoice_item_list_synopsis after delivery store department
def invoice_synopsis_sd_ad_after_del():
    c_id=session.cid
    req_depot=session.depot_id
    
    #--------------- Title
    response.title='5.1A Preview Synopsis (SD And AD) With Batch After Delivery'
    
    #-------------    
    invoice_dateFrom=''
    invoice_dateTo=''
    
    territory_id=''
    territory_name=''    
    
    d_man_id=''
    d_man_name=''
    paymentMode=''
    search_from_sl=''
    search_to_sl=''
    creditType=''
    #----------------------
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.sl!=0)
    qset=qset(db.sm_invoice_head.depot_id==req_depot)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    
    #----------
    if (session.btn_filter_printm_s):
        if session.search_dt_from!='' and session.search_dt_to!='':
            qset=qset((db.sm_invoice_head.invoice_date>=session.search_dt_from)&(db.sm_invoice_head.invoice_date<=session.search_dt_to))
            invoice_dateFrom=session.search_dt_from
            invoice_dateTo=session.search_dt_to
            
        if session.search_from_sl>0 and session.search_to_sl>0:
            qset=qset((db.sm_invoice_head.sl>=session.search_from_sl)&(db.sm_invoice_head.sl<=session.search_to_sl))
            search_from_sl=session.search_from_sl
            search_to_sl=session.search_to_sl
            
        #------------
        if (session.search_type_printm_s=='REPID'):                
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.rep_id==searchValue)
            
        elif (session.search_type_printm_s=='ROUTEID'):
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.area_id==searchValue)
            
            territory_id=searchValue
            if territory_id!='':
                areaRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id) & (db.sm_level.is_leaf == '1')).select(db.sm_level.level_name,db.sm_level.level0,db.sm_level.level0_name,limitby=(0,1))
                if areaRow:
                    territory_name=areaRow[0].level_name
                    
        elif (session.search_type_printm_s=='CLIENTID'):
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.client_id==searchValue)
        
        elif (session.search_type_printm_s=='SHIPMENT'):
            searchValue=str(session.search_value_printm_s).strip()
            qset=qset(db.sm_invoice_head.shipment_no==searchValue)
            
        #----------
        if session.print_status=='Pending':
            qset=qset(db.sm_invoice_head.field2==0)
            
        #----------
        if session.paymentMode!='':
            paymentMode=session.paymentMode
            qset=qset(db.sm_invoice_head.payment_mode==paymentMode)
            
        #----------
        if session.creditType!='':
            qset=qset(db.sm_invoice_head.credit_note==session.creditType)
            creditType=session.creditType
            
        #----------
        if not(session.d_man_id_report=='' or session.d_man_id_report==None):
            searchValue=str(session.d_man_id_report).split('|')[0]
            qset=qset(db.sm_invoice_head.d_man_id==searchValue)
            
            d_man_id=searchValue
            dmanRecords=db((db.sm_delivery_man.cid==c_id)& (db.sm_delivery_man.depot_id==req_depot) & (db.sm_delivery_man.d_man_id==d_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
            if dmanRecords:
                d_man_name=dmanRecords[0].name
    
    
    headRecords1=qset.select(db.sm_invoice_head.client_id,db.sm_invoice_head.id.count(),db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),db.sm_invoice_head.return_sp_discount.sum(),groupby=db.sm_invoice_head.client_id)
    clientCount=len(headRecords1)
    #---------------------- maximum market Name
    maxMarketID=''
    maxmarketName=''
    maxCount=0
    headRecords2=qset.select(db.sm_invoice_head.market_id,db.sm_invoice_head.market_name.max(),db.sm_invoice_head.id.count(),groupby=db.sm_invoice_head.market_id)
    for headRec2 in headRecords2:
        market_id=headRec2.sm_invoice_head.market_id
        market_name=headRec2[db.sm_invoice_head.market_name.max()]
        market_count=headRec2[db.sm_invoice_head.id.count()]        
        if market_count>maxCount:
            maxMarketID=market_id
            maxmarketName=market_name
            maxCount=market_count
        else:
            continue
    
    #------------------
    invoiceTotal=0    
    totalAmount=0
    vatTotal=0
    totalDiscount=0
    totalSpDiscount=0
    return_tp=0
    return_vat=0
    return_discount=0
    actual_total_tp=0
    return_sp_discount=0
    
    headRecords=qset.select(db.sm_invoice_head.depot_id,db.sm_invoice_head.id.count(),db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),db.sm_invoice_head.return_sp_discount.sum(),groupby=db.sm_invoice_head.depot_id)
    for hRow in headRecords:
        invoiceTotal+=hRow[db.sm_invoice_head.id.count()]
        #actual_total_tp+=hRow[db.sm_invoice_head.actual_total_tp.sum()]
        totalAmount+=hRow[db.sm_invoice_head.total_amount.sum()]
        #vatTotal+=hRow[db.sm_invoice_head.vat_total_amount.sum()]
        totalDiscount+=hRow[db.sm_invoice_head.discount.sum()]
        #totalSpDiscount+=hRow[db.sm_invoice_head.sp_discount.sum()]
        return_tp+=hRow[db.sm_invoice_head.return_tp.sum()]
        return_vat+=hRow[db.sm_invoice_head.return_vat.sum()]
        return_discount+=hRow[db.sm_invoice_head.return_discount.sum()]
        return_sp_discount+=hRow[db.sm_invoice_head.return_sp_discount.sum()]
        
    invRecords=qset((db.sm_invoice.cid==c_id) & (db.sm_invoice.depot_id==req_depot)&(db.sm_invoice_head.sl==db.sm_invoice.sl)).select(db.sm_invoice.item_id,db.sm_invoice.batch_id,db.sm_invoice.actual_tp,db.sm_invoice.price,db.sm_invoice.item_vat,db.sm_invoice.quantity.sum(),groupby=db.sm_invoice.item_id|db.sm_invoice.batch_id|db.sm_invoice.actual_tp|db.sm_invoice.price|db.sm_invoice.item_vat)      
    for invRow in invRecords:
        actualTp=invRow.sm_invoice.actual_tp
        itemRate=invRow.sm_invoice.price
        itemQty=invRow[db.sm_invoice.quantity.sum()]
        itemVat=invRow.sm_invoice.item_vat
        
        actual_total_tp+=actualTp*itemQty
        vatTotal+=itemVat*itemQty
        
        spDiscount=(actualTp-itemRate)*itemQty        
        totalSpDiscount+=spDiscount
    
    #----------
    recordsSD=qset((db.sm_invoice.cid==c_id) & (db.sm_invoice.depot_id==req_depot)&(db.sm_invoice_head.sl==db.sm_invoice.sl)).select(db.sm_invoice.item_id,db.sm_invoice.item_name.max(),db.sm_invoice.batch_id,db.sm_invoice.quantity.sum(),db.sm_invoice.bonus_qty.sum(),db.sm_invoice.return_qty.sum(),db.sm_invoice.return_bonus_qty.sum(),orderby=db.sm_invoice.item_name|db.sm_invoice.batch_id,groupby=db.sm_invoice.item_id|db.sm_invoice.batch_id)      
    
    
    #------------------
#     invoiceTotal=0    
#     totalAmount=0
#     vatTotal=0
#     totalDiscount=0
#     totalSpDiscount=0
#     return_tp=0
#     return_vat=0
#     return_discount=0
#     actual_total_tp=0
#     return_sp_discount=0
#     
#     for hRow in headRecords:
#         invoiceTotal+=hRow[db.sm_invoice_head.id.count()]
#         actual_total_tp+=hRow[db.sm_invoice_head.actual_total_tp.sum()]
#         totalAmount+=hRow[db.sm_invoice_head.total_amount.sum()]
#         vatTotal+=hRow[db.sm_invoice_head.vat_total_amount.sum()]
#         totalDiscount+=hRow[db.sm_invoice_head.discount.sum()]
#         totalSpDiscount+=hRow[db.sm_invoice_head.sp_discount.sum()]
#         return_tp+=hRow[db.sm_invoice_head.return_tp.sum()]
#         return_vat+=hRow[db.sm_invoice_head.return_vat.sum()]
#         return_discount+=hRow[db.sm_invoice_head.return_discount.sum()]
#         return_sp_discount+=hRow[db.sm_invoice_head.return_sp_discount.sum()]
        
    recordsAD=qset.select(db.sm_invoice_head.ALL,orderby=db.sm_invoice_head.sl)
    
    #-------------------------
    #return dict(records=records,maxMarketID=maxMarketID,maxmarketName=maxmarketName,paymentMode=paymentMode,creditType=creditType,search_from_sl=search_from_sl,search_to_sl=search_to_sl,territory_id=territory_id,territory_name=territory_name,invoice_dateFrom=invoice_dateFrom,invoice_dateTo=invoice_dateTo,d_man_id=d_man_id,d_man_name=d_man_name,clientCount=clientCount,invoiceTotal=invoiceTotal,actual_total_tp=actual_total_tp,return_sp_discount=return_sp_discount,totalAmount=totalAmount,vatTotal=vatTotal,totalDiscount=totalDiscount,totalSpDiscount=totalSpDiscount,return_tp=return_tp,return_vat=return_vat,return_discount=return_discount)
    
    #-------------------------
    return dict(recordsSD=recordsSD,recordsAD=recordsAD,maxMarketID=maxMarketID,maxmarketName=maxmarketName,paymentMode=paymentMode,creditType=creditType,search_from_sl=search_from_sl,search_to_sl=search_to_sl,territory_id=territory_id,territory_name=territory_name,invoice_dateFrom=invoice_dateFrom,invoice_dateTo=invoice_dateTo,d_man_id=d_man_id,d_man_name=d_man_name,clientCount=clientCount,invoiceTotal=invoiceTotal,actual_total_tp=actual_total_tp,return_sp_discount=return_sp_discount,totalAmount=totalAmount,vatTotal=vatTotal,totalDiscount=totalDiscount,totalSpDiscount=totalSpDiscount,return_tp=return_tp,return_vat=return_vat,return_discount=return_discount)
    
    

#========================= Show Invoice invoice_item_list_synopsis after delivery store department
def invoice_synopsis_sd_ad_after_del_download():
    c_id=session.cid
    req_depot=session.depot_id
    
    #--------------- Title
    response.title='5.1A Download Synopsis (SD And AD) With Batch After Delivery'
    
    #-------------    
    invoice_dateFrom=''
    invoice_dateTo=''
    
    territory_id=''
    territory_name=''    
    
    d_man_id=''
    d_man_name=''
    paymentMode=''
    search_from_sl=''
    search_to_sl=''
    creditType=''
    #----------------------
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.sl!=0)
    qset=qset(db.sm_invoice_head.depot_id==req_depot)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    
    #----------
    if (session.btn_filter_printm_s):
        if session.search_dt_from!='' and session.search_dt_to!='':
            qset=qset((db.sm_invoice_head.invoice_date>=session.search_dt_from)&(db.sm_invoice_head.invoice_date<=session.search_dt_to))
            invoice_dateFrom=session.search_dt_from
            invoice_dateTo=session.search_dt_to
            
        if session.search_from_sl>0 and session.search_to_sl>0:
            qset=qset((db.sm_invoice_head.sl>=session.search_from_sl)&(db.sm_invoice_head.sl<=session.search_to_sl))
            search_from_sl=session.search_from_sl
            search_to_sl=session.search_to_sl
            
        #------------
        if (session.search_type_printm_s=='REPID'):                
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.rep_id==searchValue)
            
        elif (session.search_type_printm_s=='ROUTEID'):
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.area_id==searchValue)
            
            territory_id=searchValue
            if territory_id!='':
                areaRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id) & (db.sm_level.is_leaf == '1')).select(db.sm_level.level_name,db.sm_level.level0,db.sm_level.level0_name,limitby=(0,1))
                if areaRow:
                    territory_name=areaRow[0].level_name
                    
        elif (session.search_type_printm_s=='CLIENTID'):
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.client_id==searchValue)
        
        elif (session.search_type_printm_s=='SHIPMENT'):
            searchValue=str(session.search_value_printm_s).strip()
            qset=qset(db.sm_invoice_head.shipment_no==searchValue)
            
        #----------
        if session.print_status=='Pending':
            qset=qset(db.sm_invoice_head.field2==0)
            
        #----------
        if session.paymentMode!='':
            paymentMode=session.paymentMode
            qset=qset(db.sm_invoice_head.payment_mode==paymentMode)
            
        #----------
        if session.creditType!='':
            qset=qset(db.sm_invoice_head.credit_note==session.creditType)
            creditType=session.creditType
            
        #----------
        if not(session.d_man_id_report=='' or session.d_man_id_report==None):
            searchValue=str(session.d_man_id_report).split('|')[0]
            qset=qset(db.sm_invoice_head.d_man_id==searchValue)
            
            d_man_id=searchValue
            dmanRecords=db((db.sm_delivery_man.cid==c_id)& (db.sm_delivery_man.depot_id==req_depot) & (db.sm_delivery_man.d_man_id==d_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
            if dmanRecords:
                d_man_name=dmanRecords[0].name
    
    
    headRecords1=qset.select(db.sm_invoice_head.client_id,db.sm_invoice_head.id.count(),db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),db.sm_invoice_head.return_sp_discount.sum(),groupby=db.sm_invoice_head.client_id)
    clientCount=len(headRecords1)
    #---------------------- maximum market Name
    maxMarketID=''
    maxmarketName=''
    maxCount=0
    headRecords2=qset.select(db.sm_invoice_head.market_id,db.sm_invoice_head.market_name.max(),db.sm_invoice_head.id.count(),groupby=db.sm_invoice_head.market_id)
    for headRec2 in headRecords2:
        market_id=headRec2.sm_invoice_head.market_id
        market_name=headRec2[db.sm_invoice_head.market_name.max()]
        market_count=headRec2[db.sm_invoice_head.id.count()]        
        if market_count>maxCount:
            maxMarketID=market_id
            maxmarketName=market_name
            maxCount=market_count
        else:
            continue
    
    #------------------
    invoiceTotal=0    
    totalAmount=0
    vatTotal=0
    totalDiscount=0
    totalSpDiscount=0
    return_tp=0
    return_vat=0
    return_discount=0
    actual_total_tp=0
    return_sp_discount=0
    
    headRecords=qset.select(db.sm_invoice_head.depot_id,db.sm_invoice_head.id.count(),db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),db.sm_invoice_head.return_sp_discount.sum(),groupby=db.sm_invoice_head.depot_id)
    for hRow in headRecords:
        invoiceTotal+=hRow[db.sm_invoice_head.id.count()]
        #actual_total_tp+=hRow[db.sm_invoice_head.actual_total_tp.sum()]
        totalAmount+=hRow[db.sm_invoice_head.total_amount.sum()]
        #vatTotal+=hRow[db.sm_invoice_head.vat_total_amount.sum()]
        totalDiscount+=hRow[db.sm_invoice_head.discount.sum()]
        #totalSpDiscount+=hRow[db.sm_invoice_head.sp_discount.sum()]
        return_tp+=hRow[db.sm_invoice_head.return_tp.sum()]
        return_vat+=hRow[db.sm_invoice_head.return_vat.sum()]
        return_discount+=hRow[db.sm_invoice_head.return_discount.sum()]
        return_sp_discount+=hRow[db.sm_invoice_head.return_sp_discount.sum()]
        
    invRecords=qset((db.sm_invoice.cid==c_id) & (db.sm_invoice.depot_id==req_depot)&(db.sm_invoice_head.sl==db.sm_invoice.sl)).select(db.sm_invoice.item_id,db.sm_invoice.batch_id,db.sm_invoice.actual_tp,db.sm_invoice.price,db.sm_invoice.item_vat,db.sm_invoice.quantity.sum(),groupby=db.sm_invoice.item_id|db.sm_invoice.batch_id|db.sm_invoice.actual_tp|db.sm_invoice.price|db.sm_invoice.item_vat)      
    for invRow in invRecords:
        actualTp=invRow.sm_invoice.actual_tp
        itemRate=invRow.sm_invoice.price
        itemQty=invRow[db.sm_invoice.quantity.sum()]
        itemVat=invRow.sm_invoice.item_vat
        
        actual_total_tp+=actualTp*itemQty
        vatTotal+=itemVat*itemQty
        
        spDiscount=(actualTp-itemRate)*itemQty        
        totalSpDiscount+=spDiscount
    
    #----------
    recordsSD=qset((db.sm_invoice.cid==c_id) & (db.sm_invoice.depot_id==req_depot)&(db.sm_invoice_head.sl==db.sm_invoice.sl)).select(db.sm_invoice.item_id,db.sm_invoice.item_name.max(),db.sm_invoice.batch_id,db.sm_invoice.quantity.sum(),db.sm_invoice.bonus_qty.sum(),db.sm_invoice.return_qty.sum(),db.sm_invoice.return_bonus_qty.sum(),orderby=db.sm_invoice.item_name|db.sm_invoice.batch_id,groupby=db.sm_invoice.item_id|db.sm_invoice.batch_id)      
    
    #------------------        
    recordsAD=qset.select(db.sm_invoice_head.ALL,orderby=db.sm_invoice_head.sl)
    
    #-------------------------
    
    #-------------------------
    if paymentMode=='':
        termsStr='ALL'
    else:
        termsStr=paymentMode
        
        if paymentMode=='CREDIT':
            if creditType=='':
                termsStr+='(ALL)'
            else:
                termsStr+='('+creditType+')'
                
    myString='(5.1A) SYNOPSIS Product Report(Store Dept) With Batch-After Delivery\n'
    myString+='SYNOPSIS (After Delivery):'+'\n'
    myString+='Market:,'+str(maxMarketID)+'|'+str(maxmarketName)+'\n'
    myString+='Delivery Person ID:,'+str(d_man_id)+'\n'
    myString+='Delivery Person Name:'+','+str(d_man_name)+'\n'
    myString+='Sales Term:,'+str(termsStr)+'\n'
    myString+='From Invoice:,'+str(search_from_sl)+'\n'
    myString+='To Invoice Range:'+','+str(search_to_sl)+'\n'
    myString+='From Date:,'+str(invoice_dateFrom)+'\n'
    myString+='To Date:,'+str(invoice_dateTo)+'\n'
    
    rowSl=0
    myString+='SL,Item ID,Item Name,Batch,Invoice-Qnty,Invoice-BonusQnty,Return-Qnty,Return-BonusQnty,Net Issue-Sold Qnty,Net Issue-Bonus Qnty'+'\n'
    for record in recordsSD:
        rowSl+=1
        
        item_id=record.sm_invoice.item_id
        item_name=str(record[db.sm_invoice.item_name.max()]).replace(',', ' ')        
        batch_id=record.sm_invoice.batch_id        
        itemQty=record[db.sm_invoice.quantity.sum()]
        bonus_qty=record[db.sm_invoice.bonus_qty.sum()]
        return_qty=record[db.sm_invoice.return_qty.sum()]
        return_bonus_qty=record[db.sm_invoice.return_bonus_qty.sum()]
        
        soldQty=record[db.sm_invoice.quantity.sum()]-record[db.sm_invoice.return_qty.sum()]
        bonusQty=record[db.sm_invoice.bonus_qty.sum()]-record[db.sm_invoice.return_bonus_qty.sum()]
        
        #------------------------        
        myString+=str(rowSl)+','+str(item_id)+','+str(item_name)+','+str(batch_id)+','+str(itemQty)+','+str(bonus_qty)+','+str(return_qty)+','+str(return_bonus_qty)+','+str(soldQty)+','+str(bonusQty)+'\n'
    
    myString+='\n\nSummary\n'
    
    myString+='DOCUMENT'+'\n'
    myString+='Invoice:,'+str(round(invoiceTotal,2))+'\n'
    myString+='Credit Note:,'+'\n'
    myString+='Debit Note:,'+'\n'
    myString+='Customer:,'+str(round(clientCount,2))+'\n\n'
    
    myString+=',INVOICE,RETURN,NET'+'\n'
    myString+='Sub Total(TP):,'+str(round(actual_total_tp,2))+',-'+str(round(return_tp+return_sp_discount,2))+','+str(round(actual_total_tp-(return_tp+return_sp_discount),2))+'\n'
    myString+='VAT:,'+str(round(vatTotal,2))+',-'+str(round(return_vat,2))+','+str(round(vatTotal-return_vat,2))+'\n'
    myString+='Discount:,'+str(round(totalDiscount,2))+',-'+str(round(return_discount,2))+','+str(round(totalDiscount-return_discount,2))+'\n'
    myString+='Special Discount:,'+str(round(totalSpDiscount,2))+',-'+str(round(return_sp_discount,2))+','+str(round(totalSpDiscount-return_sp_discount,2))+'\n'
    
    invTotal=(actual_total_tp+vatTotal-(totalDiscount+totalSpDiscount))
    totalReturn=return_tp+return_vat-return_discount
    netSale=invTotal-totalReturn
    
    myString+='Total:,'+str(round(invTotal,2))+',-'+str(round(totalReturn,2))+','+str(round(netSale,2))+'\n'
        
    inwordStr=num2word(str(round(netSale,2)))
    
    myString+='Net Sales (Taka in Words):,'+str(inwordStr)+',,,,,,,,,,,,,,,,,,,\n'
    
    myString+='\n\n\n\n\n\n'
    
    
    myString+='(5.1) SYNOPSIS Transaction Report(Acc Dept)-After Delivery\n'
    myString+='SYNOPSIS (After Delivery):'+'\n'
    myString+='Market:,'+str(maxMarketID)+'|'+str(maxmarketName)+'\n'
    myString+='Delivery Person ID:,'+str(d_man_id)+'\n'
    myString+='Delivery Person Name:'+','+str(d_man_name)+'\n'
    myString+='Sales Term:,'+str(termsStr)+'\n'
    myString+='From Invoice:,'+str(search_from_sl)+'\n'
    myString+='To Invoice Range:'+','+str(search_to_sl)+'\n'
    myString+='From Date:,'+str(invoice_dateFrom)+'\n'
    myString+='To Date:,'+str(invoice_dateTo)+'\n'
    
    total_amount=0
    
    myString+='Cust ID,Customer Name,Terms,Invoice,Date,Tp,VAT,Disc,SpDisc,Net Sale'+'\n'
    for record in recordsAD:        
        client_id=record.client_id
        client_name=str(record.client_name).replace(',', ' ')        
        payment_mode=record.payment_mode
        invSl=str(session.prefix_invoice)+'INV'+str(record.depot_id)+'-'+str(record.sl)
        invoice_date=record.invoice_date
        
        tpAmt=record.actual_total_tp-(record.return_tp+record.return_sp_discount)
        vatAmt=(record.vat_total_amount-record.return_vat)
        discAmt=(record.discount-record.return_discount)
        spDiscAmt=(record.sp_discount-record.return_sp_discount)
        totalAmt=tpAmt+vatAmt-(discAmt+spDiscAmt)
        
        total_amount+=totalAmt
        
        #------------------------        
        myString+=str(client_id)+','+str(client_name)+','+str(payment_mode)+','+str(invSl)+','+str(invoice_date)+','+str(tpAmt)+','+str(vatAmt)+','+str(discAmt)+','+str(spDiscAmt)+','+str(totalAmt)+'\n'
    
    
    myString+=str(invoiceTotal)+' Invoice(s),,,,,,,,Total:,'+str(round(total_amount,2))+'\n'
    
    
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=5.1_download_synopsisRpt_SD_AD_AfterDelivery.csv'   
    return str(myString)
    
def invoice_synopsis_sd_ad_after_del_withoutbatch():
    c_id=session.cid
    req_depot=session.depot_id
    
    #--------------- Title
    response.title='5.1B Preview Synopsis (SD And AD) Without Batch After Delivery'
    
    #-------------    
    invoice_dateFrom=''
    invoice_dateTo=''
    
    territory_id=''
    territory_name=''    
    
    d_man_id=''
    d_man_name=''
    paymentMode=''
    search_from_sl=''
    search_to_sl=''
    creditType=''
    #----------------------
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.sl!=0)
    qset=qset(db.sm_invoice_head.depot_id==req_depot)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    
    #----------
    if (session.btn_filter_printm_s):
        if session.search_dt_from!='' and session.search_dt_to!='':
            qset=qset((db.sm_invoice_head.invoice_date>=session.search_dt_from)&(db.sm_invoice_head.invoice_date<=session.search_dt_to))
            invoice_dateFrom=session.search_dt_from
            invoice_dateTo=session.search_dt_to
            
        if session.search_from_sl>0 and session.search_to_sl>0:
            qset=qset((db.sm_invoice_head.sl>=session.search_from_sl)&(db.sm_invoice_head.sl<=session.search_to_sl))
            search_from_sl=session.search_from_sl
            search_to_sl=session.search_to_sl
            
        #------------
        if (session.search_type_printm_s=='REPID'):                
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.rep_id==searchValue)
            
        elif (session.search_type_printm_s=='ROUTEID'):
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.area_id==searchValue)
            
            territory_id=searchValue
            if territory_id!='':
                areaRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id) & (db.sm_level.is_leaf == '1')).select(db.sm_level.level_name,db.sm_level.level0,db.sm_level.level0_name,limitby=(0,1))
                if areaRow:
                    territory_name=areaRow[0].level_name
                    
        elif (session.search_type_printm_s=='CLIENTID'):
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.client_id==searchValue)
        
        elif (session.search_type_printm_s=='SHIPMENT'):
            searchValue=str(session.search_value_printm_s).strip()
            qset=qset(db.sm_invoice_head.shipment_no==searchValue)
            
        #----------
        if session.print_status=='Pending':
            qset=qset(db.sm_invoice_head.field2==0)
            
        #----------
        if session.paymentMode!='':
            paymentMode=session.paymentMode
            qset=qset(db.sm_invoice_head.payment_mode==paymentMode)
            
        #----------
        if session.creditType!='':
            qset=qset(db.sm_invoice_head.credit_note==session.creditType)
            creditType=session.creditType
            
        #----------
        if not(session.d_man_id_report=='' or session.d_man_id_report==None):
            searchValue=str(session.d_man_id_report).split('|')[0]
            qset=qset(db.sm_invoice_head.d_man_id==searchValue)
            
            d_man_id=searchValue
            dmanRecords=db((db.sm_delivery_man.cid==c_id)& (db.sm_delivery_man.depot_id==req_depot) & (db.sm_delivery_man.d_man_id==d_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
            if dmanRecords:
                d_man_name=dmanRecords[0].name
    
    
    headRecords1=qset.select(db.sm_invoice_head.client_id,db.sm_invoice_head.id.count(),db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),db.sm_invoice_head.return_sp_discount.sum(),groupby=db.sm_invoice_head.client_id)
    clientCount=len(headRecords1)
    #---------------------- maximum market Name
    maxMarketID=''
    maxmarketName=''
    maxCount=0
    headRecords2=qset.select(db.sm_invoice_head.market_id,db.sm_invoice_head.market_name.max(),db.sm_invoice_head.id.count(),groupby=db.sm_invoice_head.market_id)
    for headRec2 in headRecords2:
        market_id=headRec2.sm_invoice_head.market_id
        market_name=headRec2[db.sm_invoice_head.market_name.max()]
        market_count=headRec2[db.sm_invoice_head.id.count()]        
        if market_count>maxCount:
            maxMarketID=market_id
            maxmarketName=market_name
            maxCount=market_count
        else:
            continue
    
    #------------------
    invoiceTotal=0    
    totalAmount=0
    vatTotal=0
    totalDiscount=0
    totalSpDiscount=0
    return_tp=0
    return_vat=0
    return_discount=0
    actual_total_tp=0
    return_sp_discount=0
    
    headRecords=qset.select(db.sm_invoice_head.depot_id,db.sm_invoice_head.id.count(),db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),db.sm_invoice_head.return_sp_discount.sum(),groupby=db.sm_invoice_head.depot_id)
    for hRow in headRecords:
        invoiceTotal+=hRow[db.sm_invoice_head.id.count()]
        #actual_total_tp+=hRow[db.sm_invoice_head.actual_total_tp.sum()]
        totalAmount+=hRow[db.sm_invoice_head.total_amount.sum()]
        #vatTotal+=hRow[db.sm_invoice_head.vat_total_amount.sum()]
        totalDiscount+=hRow[db.sm_invoice_head.discount.sum()]
        #totalSpDiscount+=hRow[db.sm_invoice_head.sp_discount.sum()]
        return_tp+=hRow[db.sm_invoice_head.return_tp.sum()]
        return_vat+=hRow[db.sm_invoice_head.return_vat.sum()]
        return_discount+=hRow[db.sm_invoice_head.return_discount.sum()]
        return_sp_discount+=hRow[db.sm_invoice_head.return_sp_discount.sum()]
        
    invRecords=qset((db.sm_invoice.cid==c_id) & (db.sm_invoice.depot_id==req_depot)&(db.sm_invoice_head.sl==db.sm_invoice.sl)).select(db.sm_invoice.item_id,db.sm_invoice.batch_id,db.sm_invoice.actual_tp,db.sm_invoice.price,db.sm_invoice.item_vat,db.sm_invoice.quantity.sum(),groupby=db.sm_invoice.item_id|db.sm_invoice.batch_id|db.sm_invoice.actual_tp|db.sm_invoice.price|db.sm_invoice.item_vat)      
    for invRow in invRecords:
        actualTp=invRow.sm_invoice.actual_tp
        itemRate=invRow.sm_invoice.price
        itemQty=invRow[db.sm_invoice.quantity.sum()]
        itemVat=invRow.sm_invoice.item_vat
        
        actual_total_tp+=actualTp*itemQty
        vatTotal+=itemVat*itemQty
        
        spDiscount=(actualTp-itemRate)*itemQty        
        totalSpDiscount+=spDiscount
    
    #----------
    recordsSD=qset((db.sm_invoice.cid==c_id) & (db.sm_invoice.depot_id==req_depot)&(db.sm_invoice_head.sl==db.sm_invoice.sl)).select(db.sm_invoice.item_id,db.sm_invoice.item_name.max(),db.sm_invoice.quantity.sum(),db.sm_invoice.bonus_qty.sum(),db.sm_invoice.return_qty.sum(),db.sm_invoice.return_bonus_qty.sum(),orderby=db.sm_invoice.item_name,groupby=db.sm_invoice.item_id)      
    
    #------------------
    recordsAD=qset.select(db.sm_invoice_head.ALL,orderby=db.sm_invoice_head.sl)
    
    #-------------------------
    #return dict(records=records,maxMarketID=maxMarketID,maxmarketName=maxmarketName,paymentMode=paymentMode,creditType=creditType,search_from_sl=search_from_sl,search_to_sl=search_to_sl,territory_id=territory_id,territory_name=territory_name,invoice_dateFrom=invoice_dateFrom,invoice_dateTo=invoice_dateTo,d_man_id=d_man_id,d_man_name=d_man_name,clientCount=clientCount,invoiceTotal=invoiceTotal,actual_total_tp=actual_total_tp,return_sp_discount=return_sp_discount,totalAmount=totalAmount,vatTotal=vatTotal,totalDiscount=totalDiscount,totalSpDiscount=totalSpDiscount,return_tp=return_tp,return_vat=return_vat,return_discount=return_discount)
    
    #-------------------------
    return dict(recordsSD=recordsSD,recordsAD=recordsAD,maxMarketID=maxMarketID,maxmarketName=maxmarketName,paymentMode=paymentMode,creditType=creditType,search_from_sl=search_from_sl,search_to_sl=search_to_sl,territory_id=territory_id,territory_name=territory_name,invoice_dateFrom=invoice_dateFrom,invoice_dateTo=invoice_dateTo,d_man_id=d_man_id,d_man_name=d_man_name,clientCount=clientCount,invoiceTotal=invoiceTotal,actual_total_tp=actual_total_tp,return_sp_discount=return_sp_discount,totalAmount=totalAmount,vatTotal=vatTotal,totalDiscount=totalDiscount,totalSpDiscount=totalSpDiscount,return_tp=return_tp,return_vat=return_vat,return_discount=return_discount)
    
#========================= Show Invoice invoice_item_list_synopsis after delivery store department
def invoice_synopsis_sd_ad_after_del_withoutbatch_download():
    c_id=session.cid
    req_depot=session.depot_id
    
    #--------------- Title
    response.title='5.1B Download Synopsis (SD And AD) Without Batch After Delivery'
    
    #-------------    
    invoice_dateFrom=''
    invoice_dateTo=''
    
    territory_id=''
    territory_name=''    
    
    d_man_id=''
    d_man_name=''
    paymentMode=''
    search_from_sl=''
    search_to_sl=''
    creditType=''
    #----------------------
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.sl!=0)
    qset=qset(db.sm_invoice_head.depot_id==req_depot)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    
    #----------
    if (session.btn_filter_printm_s):
        if session.search_dt_from!='' and session.search_dt_to!='':
            qset=qset((db.sm_invoice_head.invoice_date>=session.search_dt_from)&(db.sm_invoice_head.invoice_date<=session.search_dt_to))
            invoice_dateFrom=session.search_dt_from
            invoice_dateTo=session.search_dt_to
            
        if session.search_from_sl>0 and session.search_to_sl>0:
            qset=qset((db.sm_invoice_head.sl>=session.search_from_sl)&(db.sm_invoice_head.sl<=session.search_to_sl))
            search_from_sl=session.search_from_sl
            search_to_sl=session.search_to_sl
            
        #------------
        if (session.search_type_printm_s=='REPID'):                
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.rep_id==searchValue)
            
        elif (session.search_type_printm_s=='ROUTEID'):
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.area_id==searchValue)
            
            territory_id=searchValue
            if territory_id!='':
                areaRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id) & (db.sm_level.is_leaf == '1')).select(db.sm_level.level_name,db.sm_level.level0,db.sm_level.level0_name,limitby=(0,1))
                if areaRow:
                    territory_name=areaRow[0].level_name
                    
        elif (session.search_type_printm_s=='CLIENTID'):
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.client_id==searchValue)
        
        elif (session.search_type_printm_s=='SHIPMENT'):
            searchValue=str(session.search_value_printm_s).strip()
            qset=qset(db.sm_invoice_head.shipment_no==searchValue)
            
        #----------
        if session.print_status=='Pending':
            qset=qset(db.sm_invoice_head.field2==0)
            
        #----------
        if session.paymentMode!='':
            paymentMode=session.paymentMode
            qset=qset(db.sm_invoice_head.payment_mode==paymentMode)
            
        #----------
        if session.creditType!='':
            qset=qset(db.sm_invoice_head.credit_note==session.creditType)
            creditType=session.creditType
            
        #----------
        if not(session.d_man_id_report=='' or session.d_man_id_report==None):
            searchValue=str(session.d_man_id_report).split('|')[0]
            qset=qset(db.sm_invoice_head.d_man_id==searchValue)
            
            d_man_id=searchValue
            dmanRecords=db((db.sm_delivery_man.cid==c_id)& (db.sm_delivery_man.depot_id==req_depot) & (db.sm_delivery_man.d_man_id==d_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
            if dmanRecords:
                d_man_name=dmanRecords[0].name
    
    
    headRecords1=qset.select(db.sm_invoice_head.client_id,db.sm_invoice_head.id.count(),db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),db.sm_invoice_head.return_sp_discount.sum(),groupby=db.sm_invoice_head.client_id)
    clientCount=len(headRecords1)
    #---------------------- maximum market Name
    maxMarketID=''
    maxmarketName=''
    maxCount=0
    headRecords2=qset.select(db.sm_invoice_head.market_id,db.sm_invoice_head.market_name.max(),db.sm_invoice_head.id.count(),groupby=db.sm_invoice_head.market_id)
    for headRec2 in headRecords2:
        market_id=headRec2.sm_invoice_head.market_id
        market_name=headRec2[db.sm_invoice_head.market_name.max()]
        market_count=headRec2[db.sm_invoice_head.id.count()]        
        if market_count>maxCount:
            maxMarketID=market_id
            maxmarketName=market_name
            maxCount=market_count
        else:
            continue
    
    #------------------
    invoiceTotal=0    
    totalAmount=0
    vatTotal=0
    totalDiscount=0
    totalSpDiscount=0
    return_tp=0
    return_vat=0
    return_discount=0
    actual_total_tp=0
    return_sp_discount=0
    
    headRecords=qset.select(db.sm_invoice_head.depot_id,db.sm_invoice_head.id.count(),db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),db.sm_invoice_head.return_sp_discount.sum(),groupby=db.sm_invoice_head.depot_id)
    for hRow in headRecords:
        invoiceTotal+=hRow[db.sm_invoice_head.id.count()]
        #actual_total_tp+=hRow[db.sm_invoice_head.actual_total_tp.sum()]
        totalAmount+=hRow[db.sm_invoice_head.total_amount.sum()]
        #vatTotal+=hRow[db.sm_invoice_head.vat_total_amount.sum()]
        totalDiscount+=hRow[db.sm_invoice_head.discount.sum()]
        #totalSpDiscount+=hRow[db.sm_invoice_head.sp_discount.sum()]
        return_tp+=hRow[db.sm_invoice_head.return_tp.sum()]
        return_vat+=hRow[db.sm_invoice_head.return_vat.sum()]
        return_discount+=hRow[db.sm_invoice_head.return_discount.sum()]
        return_sp_discount+=hRow[db.sm_invoice_head.return_sp_discount.sum()]
        
    invRecords=qset((db.sm_invoice.cid==c_id) & (db.sm_invoice.depot_id==req_depot)&(db.sm_invoice_head.sl==db.sm_invoice.sl)).select(db.sm_invoice.item_id,db.sm_invoice.batch_id,db.sm_invoice.actual_tp,db.sm_invoice.price,db.sm_invoice.item_vat,db.sm_invoice.quantity.sum(),groupby=db.sm_invoice.item_id|db.sm_invoice.batch_id|db.sm_invoice.actual_tp|db.sm_invoice.price|db.sm_invoice.item_vat)      
    for invRow in invRecords:
        actualTp=invRow.sm_invoice.actual_tp
        itemRate=invRow.sm_invoice.price
        itemQty=invRow[db.sm_invoice.quantity.sum()]
        itemVat=invRow.sm_invoice.item_vat
        
        actual_total_tp+=actualTp*itemQty
        vatTotal+=itemVat*itemQty
        
        spDiscount=(actualTp-itemRate)*itemQty        
        totalSpDiscount+=spDiscount
        
    #----------
    recordsSD=qset((db.sm_invoice.cid==c_id) & (db.sm_invoice.depot_id==req_depot)&(db.sm_invoice_head.sl==db.sm_invoice.sl)).select(db.sm_invoice.item_id,db.sm_invoice.item_name.max(),db.sm_invoice.quantity.sum(),db.sm_invoice.bonus_qty.sum(),db.sm_invoice.return_qty.sum(),db.sm_invoice.return_bonus_qty.sum(),orderby=db.sm_invoice.item_name,groupby=db.sm_invoice.item_id)      
    
    #------------------        
    recordsAD=qset.select(db.sm_invoice_head.ALL,orderby=db.sm_invoice_head.sl)
    
    #-------------------------
    
    #-------------------------
    if paymentMode=='':
        termsStr='ALL'
    else:
        termsStr=paymentMode
        
        if paymentMode=='CREDIT':
            if creditType=='':
                termsStr+='(ALL)'
            else:
                termsStr+='('+creditType+')'
    
    myString='(5.1B) SYNOPSIS Product Report(Store Dept) Without Batch-After Delivery\n'
    myString+='SYNOPSIS (After Delivery):'+'\n'
    myString+='Market:,'+str(maxMarketID)+'|'+str(maxmarketName)+'\n'
    myString+='Delivery Person ID:,'+str(d_man_id)+'\n'
    myString+='Delivery Person Name:'+','+str(d_man_name)+'\n'
    myString+='Sales Term:,'+str(termsStr)+'\n'
    myString+='From Invoice:,'+str(search_from_sl)+'\n'
    myString+='To Invoice Range:'+','+str(search_to_sl)+'\n'
    myString+='From Date:,'+str(invoice_dateFrom)+'\n'
    myString+='To Date:,'+str(invoice_dateTo)+'\n'
    
    rowSl=0
    myString+='SL,Item ID,Item Name,Invoice-Qnty,Invoice-BonusQnty,Return-Qnty,Return-BonusQnty,Net Issue-Sold Qnty,Net Issue-Bonus Qnty'+'\n'
    for record in recordsSD:
        rowSl+=1
        
        item_id=record.sm_invoice.item_id
        item_name=str(record[db.sm_invoice.item_name.max()]).replace(',', ' ')        
             
        itemQty=record[db.sm_invoice.quantity.sum()]
        bonus_qty=record[db.sm_invoice.bonus_qty.sum()]
        return_qty=record[db.sm_invoice.return_qty.sum()]
        return_bonus_qty=record[db.sm_invoice.return_bonus_qty.sum()]
        
        soldQty=record[db.sm_invoice.quantity.sum()]-record[db.sm_invoice.return_qty.sum()]
        bonusQty=record[db.sm_invoice.bonus_qty.sum()]-record[db.sm_invoice.return_bonus_qty.sum()]
        
        #------------------------        
        myString+=str(rowSl)+','+str(item_id)+','+str(item_name)+','+str(itemQty)+','+str(bonus_qty)+','+str(return_qty)+','+str(return_bonus_qty)+','+str(soldQty)+','+str(bonusQty)+'\n'
    
    myString+='\n\nSummary\n'
    
    myString+='DOCUMENT'+'\n'
    myString+='Invoice:,'+str(round(invoiceTotal,2))+'\n'
    myString+='Credit Note:,'+'\n'
    myString+='Debit Note:,'+'\n'
    myString+='Customer:,'+str(round(clientCount,2))+'\n\n'
    
    myString+=',INVOICE,RETURN,NET'+'\n'
    myString+='Sub Total(TP):,'+str(round(actual_total_tp,2))+',-'+str(round(return_tp+return_sp_discount,2))+','+str(round(actual_total_tp-(return_tp+return_sp_discount),2))+'\n'
    myString+='VAT:,'+str(round(vatTotal,2))+',-'+str(round(return_vat,2))+','+str(round(vatTotal-return_vat,2))+'\n'
    myString+='Discount:,'+str(round(totalDiscount,2))+',-'+str(round(return_discount,2))+','+str(round(totalDiscount-return_discount,2))+'\n'
    myString+='Special Discount:,'+str(round(totalSpDiscount,2))+',-'+str(round(return_sp_discount,2))+','+str(round(totalSpDiscount-return_sp_discount,2))+'\n'
    
    invTotal=(actual_total_tp+vatTotal-(totalDiscount+totalSpDiscount))
    totalReturn=return_tp+return_vat-return_discount
    netSale=invTotal-totalReturn
    
    myString+='Total:,'+str(round(invTotal,2))+',-'+str(round(totalReturn,2))+','+str(round(netSale,2))+'\n'
        
    inwordStr=num2word(str(round(netSale,2)))
    
    myString+='Net Sales (Taka in Words):,'+str(inwordStr)+',,,,,,,,,,,,,,,,,,,\n'
    
    myString+='\n\n\n\n\n\n'
    
    
    myString+='(5.1) SYNOPSIS Transaction Report(Acc Dept)-After Delivery\n'
    myString+='SYNOPSIS (After Delivery):'+'\n'
    myString+='Market:,'+str(maxMarketID)+'|'+str(maxmarketName)+'\n'
    myString+='Delivery Person ID:,'+str(d_man_id)+'\n'
    myString+='Delivery Person Name:'+','+str(d_man_name)+'\n'
    myString+='Sales Term:,'+str(termsStr)+'\n'
    myString+='From Invoice:,'+str(search_from_sl)+'\n'
    myString+='To Invoice Range:'+','+str(search_to_sl)+'\n'
    myString+='From Date:,'+str(invoice_dateFrom)+'\n'
    myString+='To Date:,'+str(invoice_dateTo)+'\n'
    
    total_amount=0
    
    myString+='Cust ID,Customer Name,Terms,Invoice,Date,Tp,VAT,Disc,SpDisc,Net Sale'+'\n'
    for record in recordsAD:        
        client_id=record.client_id
        client_name=str(record.client_name).replace(',', ' ')        
        payment_mode=record.payment_mode
        invSl=str(session.prefix_invoice)+'INV'+str(record.depot_id)+'-'+str(record.sl)
        invoice_date=record.invoice_date
        
        tpAmt=record.actual_total_tp-(record.return_tp+record.return_sp_discount)
        vatAmt=(record.vat_total_amount-record.return_vat)
        discAmt=(record.discount-record.return_discount)
        spDiscAmt=(record.sp_discount-record.return_sp_discount)
        totalAmt=tpAmt+vatAmt-(discAmt+spDiscAmt)
        
        total_amount+=totalAmt
        
        #------------------------        
        myString+=str(client_id)+','+str(client_name)+','+str(payment_mode)+','+str(invSl)+','+str(invoice_date)+','+str(tpAmt)+','+str(vatAmt)+','+str(discAmt)+','+str(spDiscAmt)+','+str(totalAmt)+'\n'
    
    
    myString+=str(invoiceTotal)+' Invoice(s),,,,,,,,Total:,'+str(round(total_amount,2))+'\n'
    
    
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=5.1_download_synopsisRpt_SD_AD_AfterDelivery.csv'   
    return str(myString)
    


def invoice_synopsis_sd_ad_after_del_withoutbatch_retDet():
    c_id=session.cid
    req_depot=session.depot_id
    
    #--------------- Title
    response.title='5.1C Preview Synopsis (SD And AD) Without Batch After Delivery With Return Details'
    
    #-------------    
    invoice_dateFrom=''
    invoice_dateTo=''
    
    territory_id=''
    territory_name=''    
    
    d_man_id=''
    d_man_name=''
    paymentMode=''
    search_from_sl=''
    search_to_sl=''
    creditType=''
    #----------------------
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.sl!=0)
    qset=qset(db.sm_invoice_head.depot_id==req_depot)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    
    #----------
    if (session.btn_filter_printm_s):
        if session.search_dt_from!='' and session.search_dt_to!='':
            qset=qset((db.sm_invoice_head.invoice_date>=session.search_dt_from)&(db.sm_invoice_head.invoice_date<=session.search_dt_to))
            invoice_dateFrom=session.search_dt_from
            invoice_dateTo=session.search_dt_to
            
        if session.search_from_sl>0 and session.search_to_sl>0:
            qset=qset((db.sm_invoice_head.sl>=session.search_from_sl)&(db.sm_invoice_head.sl<=session.search_to_sl))
            search_from_sl=session.search_from_sl
            search_to_sl=session.search_to_sl
            
        #------------
        if (session.search_type_printm_s=='REPID'):                
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.rep_id==searchValue)
            
        elif (session.search_type_printm_s=='ROUTEID'):
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.area_id==searchValue)
            
            territory_id=searchValue
            if territory_id!='':
                areaRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id) & (db.sm_level.is_leaf == '1')).select(db.sm_level.level_name,db.sm_level.level0,db.sm_level.level0_name,limitby=(0,1))
                if areaRow:
                    territory_name=areaRow[0].level_name
                    
        elif (session.search_type_printm_s=='CLIENTID'):
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.client_id==searchValue)
        
        elif (session.search_type_printm_s=='SHIPMENT'):
            searchValue=str(session.search_value_printm_s).strip()
            qset=qset(db.sm_invoice_head.shipment_no==searchValue)
            
        #----------
        if session.print_status=='Pending':
            qset=qset(db.sm_invoice_head.field2==0)
            
        #----------
        if session.paymentMode!='':
            paymentMode=session.paymentMode
            qset=qset(db.sm_invoice_head.payment_mode==paymentMode)
            
        #----------
        if session.creditType!='':
            qset=qset(db.sm_invoice_head.credit_note==session.creditType)
            creditType=session.creditType
            
        #----------
        if not(session.d_man_id_report=='' or session.d_man_id_report==None):
            searchValue=str(session.d_man_id_report).split('|')[0]
            qset=qset(db.sm_invoice_head.d_man_id==searchValue)
            
            d_man_id=searchValue
            dmanRecords=db((db.sm_delivery_man.cid==c_id)& (db.sm_delivery_man.depot_id==req_depot) & (db.sm_delivery_man.d_man_id==d_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
            if dmanRecords:
                d_man_name=dmanRecords[0].name
    
    
    headRecords1=qset.select(db.sm_invoice_head.client_id,db.sm_invoice_head.id.count(),db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),db.sm_invoice_head.return_sp_discount.sum(),groupby=db.sm_invoice_head.client_id)
    clientCount=len(headRecords1)
    #---------------------- maximum market Name
    maxMarketID=''
    maxmarketName=''
    maxCount=0
    headRecords2=qset.select(db.sm_invoice_head.market_id,db.sm_invoice_head.market_name.max(),db.sm_invoice_head.id.count(),groupby=db.sm_invoice_head.market_id)
    for headRec2 in headRecords2:
        market_id=headRec2.sm_invoice_head.market_id
        market_name=headRec2[db.sm_invoice_head.market_name.max()]
        market_count=headRec2[db.sm_invoice_head.id.count()]        
        if market_count>maxCount:
            maxMarketID=market_id
            maxmarketName=market_name
            maxCount=market_count
        else:
            continue
    
    #------------------
    invoiceTotal=0    
    totalAmount=0
    vatTotal=0
    totalDiscount=0
    totalSpDiscount=0
    return_tp=0
    return_vat=0
    return_discount=0
    actual_total_tp=0
    return_sp_discount=0
    
    headRecords=qset.select(db.sm_invoice_head.depot_id,db.sm_invoice_head.id.count(),db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),db.sm_invoice_head.return_sp_discount.sum(),groupby=db.sm_invoice_head.depot_id)
    for hRow in headRecords:
        invoiceTotal+=hRow[db.sm_invoice_head.id.count()]
        #actual_total_tp+=hRow[db.sm_invoice_head.actual_total_tp.sum()]
        totalAmount+=hRow[db.sm_invoice_head.total_amount.sum()]
        #vatTotal+=hRow[db.sm_invoice_head.vat_total_amount.sum()]
        totalDiscount+=hRow[db.sm_invoice_head.discount.sum()]
        #totalSpDiscount+=hRow[db.sm_invoice_head.sp_discount.sum()]
        return_tp+=hRow[db.sm_invoice_head.return_tp.sum()]
        return_vat+=hRow[db.sm_invoice_head.return_vat.sum()]
        return_discount+=hRow[db.sm_invoice_head.return_discount.sum()]
        return_sp_discount+=hRow[db.sm_invoice_head.return_sp_discount.sum()]
        
    invRecords=qset((db.sm_invoice.cid==c_id) & (db.sm_invoice.depot_id==req_depot)&(db.sm_invoice_head.sl==db.sm_invoice.sl)).select(db.sm_invoice.item_id,db.sm_invoice.batch_id,db.sm_invoice.actual_tp,db.sm_invoice.price,db.sm_invoice.item_vat,db.sm_invoice.quantity.sum(),groupby=db.sm_invoice.item_id|db.sm_invoice.batch_id|db.sm_invoice.actual_tp|db.sm_invoice.price|db.sm_invoice.item_vat)      
    for invRow in invRecords:
        actualTp=invRow.sm_invoice.actual_tp
        itemRate=invRow.sm_invoice.price
        itemQty=invRow[db.sm_invoice.quantity.sum()]
        itemVat=invRow.sm_invoice.item_vat
        
        actual_total_tp+=actualTp*itemQty
        vatTotal+=itemVat*itemQty
        
        spDiscount=(actualTp-itemRate)*itemQty        
        totalSpDiscount+=spDiscount
    
    #----------
    recordsSD=qset((db.sm_invoice.cid==c_id) & (db.sm_invoice.depot_id==req_depot)&(db.sm_invoice_head.sl==db.sm_invoice.sl)).select(db.sm_invoice.item_id,db.sm_invoice.item_name.max(),db.sm_invoice.quantity.sum(),db.sm_invoice.bonus_qty.sum(),db.sm_invoice.return_qty.sum(),db.sm_invoice.return_bonus_qty.sum(),orderby=db.sm_invoice.item_name,groupby=db.sm_invoice.item_id)      
    
    #------------------
    recordsAD=qset.select(db.sm_invoice_head.ALL,orderby=db.sm_invoice_head.sl)
    
    #-------------------------
    
    qset=qset(db.sm_return_head.cid==c_id)    
    qset=qset(db.sm_return_head.depot_id==req_depot)
    qset=qset(db.sm_return_head.status=='Returned')
    qset=qset(db.sm_invoice_head.sl==db.sm_return_head.invoice_sl)    
    retRecords=qset.select(db.sm_return_head.depot_id,db.sm_return_head.sl,db.sm_return_head.return_date,db.sm_return_head.invoice_sl,db.sm_return_head.ret_actual_total_tp,db.sm_return_head.total_amount,db.sm_return_head.vat_total_amount,db.sm_return_head.discount,db.sm_return_head.sp_discount,orderby=db.sm_return_head.invoice_sl)
    returnList=retRecords.as_list()
    
    #-------------------------
    return dict(recordsSD=recordsSD,returnList=returnList,recordsAD=recordsAD,maxMarketID=maxMarketID,maxmarketName=maxmarketName,paymentMode=paymentMode,creditType=creditType,search_from_sl=search_from_sl,search_to_sl=search_to_sl,territory_id=territory_id,territory_name=territory_name,invoice_dateFrom=invoice_dateFrom,invoice_dateTo=invoice_dateTo,d_man_id=d_man_id,d_man_name=d_man_name,clientCount=clientCount,invoiceTotal=invoiceTotal,actual_total_tp=actual_total_tp,return_sp_discount=return_sp_discount,totalAmount=totalAmount,vatTotal=vatTotal,totalDiscount=totalDiscount,totalSpDiscount=totalSpDiscount,return_tp=return_tp,return_vat=return_vat,return_discount=return_discount)
    
#========================= Show Invoice invoice_item_list_synopsis after delivery store department
def invoice_synopsis_sd_ad_after_del_withoutbatch_retDet_download():
    c_id=session.cid
    req_depot=session.depot_id
    
    #--------------- Title
    response.title='5.1C Download Synopsis (SD And AD) Without Batch After Delivery With Return Details'
    
    #-------------    
    invoice_dateFrom=''
    invoice_dateTo=''
    
    territory_id=''
    territory_name=''    
    
    d_man_id=''
    d_man_name=''
    paymentMode=''
    search_from_sl=''
    search_to_sl=''
    creditType=''
    #----------------------
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.sl!=0)
    qset=qset(db.sm_invoice_head.depot_id==req_depot)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    
    #----------
    if (session.btn_filter_printm_s):
        if session.search_dt_from!='' and session.search_dt_to!='':
            qset=qset((db.sm_invoice_head.invoice_date>=session.search_dt_from)&(db.sm_invoice_head.invoice_date<=session.search_dt_to))
            invoice_dateFrom=session.search_dt_from
            invoice_dateTo=session.search_dt_to
            
        if session.search_from_sl>0 and session.search_to_sl>0:
            qset=qset((db.sm_invoice_head.sl>=session.search_from_sl)&(db.sm_invoice_head.sl<=session.search_to_sl))
            search_from_sl=session.search_from_sl
            search_to_sl=session.search_to_sl
            
        #------------
        if (session.search_type_printm_s=='REPID'):                
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.rep_id==searchValue)
            
        elif (session.search_type_printm_s=='ROUTEID'):
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.area_id==searchValue)
            
            territory_id=searchValue
            if territory_id!='':
                areaRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==territory_id) & (db.sm_level.is_leaf == '1')).select(db.sm_level.level_name,db.sm_level.level0,db.sm_level.level0_name,limitby=(0,1))
                if areaRow:
                    territory_name=areaRow[0].level_name
                    
        elif (session.search_type_printm_s=='CLIENTID'):
            searchValue=str(session.search_value_printm_s).split('|')[0]
            qset=qset(db.sm_invoice_head.client_id==searchValue)
        
        elif (session.search_type_printm_s=='SHIPMENT'):
            searchValue=str(session.search_value_printm_s).strip()
            qset=qset(db.sm_invoice_head.shipment_no==searchValue)
            
        #----------
        if session.print_status=='Pending':
            qset=qset(db.sm_invoice_head.field2==0)
            
        #----------
        if session.paymentMode!='':
            paymentMode=session.paymentMode
            qset=qset(db.sm_invoice_head.payment_mode==paymentMode)
            
        #----------
        if session.creditType!='':
            qset=qset(db.sm_invoice_head.credit_note==session.creditType)
            creditType=session.creditType
            
        #----------
        if not(session.d_man_id_report=='' or session.d_man_id_report==None):
            searchValue=str(session.d_man_id_report).split('|')[0]
            qset=qset(db.sm_invoice_head.d_man_id==searchValue)
            
            d_man_id=searchValue
            dmanRecords=db((db.sm_delivery_man.cid==c_id)& (db.sm_delivery_man.depot_id==req_depot) & (db.sm_delivery_man.d_man_id==d_man_id)).select(db.sm_delivery_man.name,limitby=(0,1))
            if dmanRecords:
                d_man_name=dmanRecords[0].name
    
    
    headRecords1=qset.select(db.sm_invoice_head.client_id,db.sm_invoice_head.id.count(),db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),db.sm_invoice_head.return_sp_discount.sum(),groupby=db.sm_invoice_head.client_id)
    clientCount=len(headRecords1)
    #---------------------- maximum market Name
    maxMarketID=''
    maxmarketName=''
    maxCount=0
    headRecords2=qset.select(db.sm_invoice_head.market_id,db.sm_invoice_head.market_name.max(),db.sm_invoice_head.id.count(),groupby=db.sm_invoice_head.market_id)
    for headRec2 in headRecords2:
        market_id=headRec2.sm_invoice_head.market_id
        market_name=headRec2[db.sm_invoice_head.market_name.max()]
        market_count=headRec2[db.sm_invoice_head.id.count()]        
        if market_count>maxCount:
            maxMarketID=market_id
            maxmarketName=market_name
            maxCount=market_count
        else:
            continue
    
    #------------------
    invoiceTotal=0    
    totalAmount=0
    vatTotal=0
    totalDiscount=0
    totalSpDiscount=0
    return_tp=0
    return_vat=0
    return_discount=0
    actual_total_tp=0
    return_sp_discount=0
    
    headRecords=qset.select(db.sm_invoice_head.depot_id,db.sm_invoice_head.id.count(),db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),db.sm_invoice_head.return_sp_discount.sum(),groupby=db.sm_invoice_head.depot_id)
    for hRow in headRecords:
        invoiceTotal+=hRow[db.sm_invoice_head.id.count()]
        #actual_total_tp+=hRow[db.sm_invoice_head.actual_total_tp.sum()]
        totalAmount+=hRow[db.sm_invoice_head.total_amount.sum()]
        #vatTotal+=hRow[db.sm_invoice_head.vat_total_amount.sum()]
        totalDiscount+=hRow[db.sm_invoice_head.discount.sum()]
        #totalSpDiscount+=hRow[db.sm_invoice_head.sp_discount.sum()]
        return_tp+=hRow[db.sm_invoice_head.return_tp.sum()]
        return_vat+=hRow[db.sm_invoice_head.return_vat.sum()]
        return_discount+=hRow[db.sm_invoice_head.return_discount.sum()]
        return_sp_discount+=hRow[db.sm_invoice_head.return_sp_discount.sum()]
        
    invRecords=qset((db.sm_invoice.cid==c_id) & (db.sm_invoice.depot_id==req_depot)&(db.sm_invoice_head.sl==db.sm_invoice.sl)).select(db.sm_invoice.item_id,db.sm_invoice.batch_id,db.sm_invoice.actual_tp,db.sm_invoice.price,db.sm_invoice.item_vat,db.sm_invoice.quantity.sum(),groupby=db.sm_invoice.item_id|db.sm_invoice.batch_id|db.sm_invoice.actual_tp|db.sm_invoice.price|db.sm_invoice.item_vat)      
    for invRow in invRecords:
        actualTp=invRow.sm_invoice.actual_tp
        itemRate=invRow.sm_invoice.price
        itemQty=invRow[db.sm_invoice.quantity.sum()]
        itemVat=invRow.sm_invoice.item_vat
        
        actual_total_tp+=actualTp*itemQty
        vatTotal+=itemVat*itemQty
        
        spDiscount=(actualTp-itemRate)*itemQty        
        totalSpDiscount+=spDiscount
        
    #----------
    recordsSD=qset((db.sm_invoice.cid==c_id) & (db.sm_invoice.depot_id==req_depot)&(db.sm_invoice_head.sl==db.sm_invoice.sl)).select(db.sm_invoice.item_id,db.sm_invoice.item_name.max(),db.sm_invoice.quantity.sum(),db.sm_invoice.bonus_qty.sum(),db.sm_invoice.return_qty.sum(),db.sm_invoice.return_bonus_qty.sum(),orderby=db.sm_invoice.item_name,groupby=db.sm_invoice.item_id)      
    
    #------------------        
    recordsAD=qset.select(db.sm_invoice_head.ALL,orderby=db.sm_invoice_head.sl)
    
    #-------------------------
    qset=qset(db.sm_return_head.cid==c_id)    
    qset=qset(db.sm_return_head.depot_id==req_depot)
    qset=qset(db.sm_return_head.status=='Returned')
    qset=qset(db.sm_invoice_head.sl==db.sm_return_head.invoice_sl)    
    retRecords=qset.select(db.sm_return_head.depot_id,db.sm_return_head.sl,db.sm_return_head.return_date,db.sm_return_head.invoice_sl,db.sm_return_head.ret_actual_total_tp,db.sm_return_head.total_amount,db.sm_return_head.vat_total_amount,db.sm_return_head.discount,db.sm_return_head.sp_discount,orderby=db.sm_return_head.invoice_sl)
    returnList=retRecords.as_list()
    
    
    #-------------------------
    if paymentMode=='':
        termsStr='ALL'
    else:
        termsStr=paymentMode
        
        if paymentMode=='CREDIT':
            if creditType=='':
                termsStr+='(ALL)'
            else:
                termsStr+='('+creditType+')'
    
    myString='(5.1C) SYNOPSIS Product Report(Store Dept) Without Batch-After Delivery\n'
    myString+='SYNOPSIS (After Delivery):'+'\n'
    myString+='Market:,'+str(maxMarketID)+'|'+str(maxmarketName)+'\n'
    myString+='Delivery Person ID:,'+str(d_man_id)+'\n'
    myString+='Delivery Person Name:'+','+str(d_man_name)+'\n'
    myString+='Sales Term:,'+str(termsStr)+'\n'
    myString+='From Invoice:,'+str(search_from_sl)+'\n'
    myString+='To Invoice Range:'+','+str(search_to_sl)+'\n'
    myString+='From Date:,'+str(invoice_dateFrom)+'\n'
    myString+='To Date:,'+str(invoice_dateTo)+'\n'
    
    rowSl=0
    myString+='SL,Item ID,Item Name,Invoice-Qnty,Invoice-BonusQnty,Return-Qnty,Return-BonusQnty,Net Issue-Sold Qnty,Net Issue-Bonus Qnty'+'\n'
    for record in recordsSD:
        rowSl+=1
        
        item_id=record.sm_invoice.item_id
        item_name=str(record[db.sm_invoice.item_name.max()]).replace(',', ' ')        
             
        itemQty=record[db.sm_invoice.quantity.sum()]
        bonus_qty=record[db.sm_invoice.bonus_qty.sum()]
        return_qty=record[db.sm_invoice.return_qty.sum()]
        return_bonus_qty=record[db.sm_invoice.return_bonus_qty.sum()]
        
        soldQty=record[db.sm_invoice.quantity.sum()]-record[db.sm_invoice.return_qty.sum()]
        bonusQty=record[db.sm_invoice.bonus_qty.sum()]-record[db.sm_invoice.return_bonus_qty.sum()]
        
        #------------------------        
        myString+=str(rowSl)+','+str(item_id)+','+str(item_name)+','+str(itemQty)+','+str(bonus_qty)+','+str(return_qty)+','+str(return_bonus_qty)+','+str(soldQty)+','+str(bonusQty)+'\n'
    
    myString+='\n\nSummary\n'
    
    myString+='DOCUMENT'+'\n'
    myString+='Invoice:,'+str(round(invoiceTotal,2))+'\n'
    myString+='Credit Note:,'+'\n'
    myString+='Debit Note:,'+'\n'
    myString+='Customer:,'+str(round(clientCount,2))+'\n\n'
    
    myString+=',INVOICE,RETURN,NET'+'\n'
    myString+='Sub Total(TP):,'+str(round(actual_total_tp,2))+',-'+str(round(return_tp+return_sp_discount,2))+','+str(round(actual_total_tp-(return_tp+return_sp_discount),2))+'\n'
    myString+='VAT:,'+str(round(vatTotal,2))+',-'+str(round(return_vat,2))+','+str(round(vatTotal-return_vat,2))+'\n'
    myString+='Discount:,'+str(round(totalDiscount,2))+',-'+str(round(return_discount,2))+','+str(round(totalDiscount-return_discount,2))+'\n'
    myString+='Special Discount:,'+str(round(totalSpDiscount,2))+',-'+str(round(return_sp_discount,2))+','+str(round(totalSpDiscount-return_sp_discount,2))+'\n'
    
    invTotal=(actual_total_tp+vatTotal-(totalDiscount+totalSpDiscount))
    totalReturn=return_tp+return_vat-return_discount
    netSale=invTotal-totalReturn
    
    myString+='Total:,'+str(round(invTotal,2))+',-'+str(round(totalReturn,2))+','+str(round(netSale,2))+'\n'
        
    inwordStr=num2word(str(round(netSale,2)))
    
    myString+='Net Sales (Taka in Words):,'+str(inwordStr)+',,,,,,,,,,,,,,,,,,,\n'
    
    myString+='\n\n\n\n\n\n'
    
    
    myString+='(5.1) SYNOPSIS Transaction Report(Acc Dept)-After Delivery With Return Details\n'
    myString+='SYNOPSIS (After Delivery):'+'\n'
    myString+='Market:,'+str(maxMarketID)+'|'+str(maxmarketName)+'\n'
    myString+='Delivery Person ID:,'+str(d_man_id)+'\n'
    myString+='Delivery Person Name:'+','+str(d_man_name)+'\n'
    myString+='Sales Term:,'+str(termsStr)+'\n'
    myString+='From Invoice:,'+str(search_from_sl)+'\n'
    myString+='To Invoice Range:'+','+str(search_to_sl)+'\n'
    myString+='From Date:,'+str(invoice_dateFrom)+'\n'
    myString+='To Date:,'+str(invoice_dateTo)+'\n'
    
    total_amount=0
    
    myString+='Cust ID,Customer Name,Terms,Shipment No,Date,Ref.No,Tp,VAT,Disc,SpDisc,Net Sale'+'\n'
    for record in recordsAD:        
        client_id=record.client_id
        client_name=str(record.client_name).replace(',', ' ')        
        payment_mode=record.payment_mode
        invSl=str(session.prefix_invoice)+'INV'+str(record.depot_id)+'-'+str(record.sl)
        invoice_date=record.invoice_date
        shipment_no=record.shipment_no
        
        actual_total_tp=record.actual_total_tp
        vat_total_amount=record.vat_total_amount
        discount=record.discount
        sp_discount=record.sp_discount
        
        tpAmt=record.actual_total_tp-(record.return_tp+record.return_sp_discount)
        vatAmt=(record.vat_total_amount-record.return_vat)
        discAmt=(record.discount-record.return_discount)
        spDiscAmt=(record.sp_discount-record.return_sp_discount)
        totalAmt=tpAmt+vatAmt-(discAmt+spDiscAmt)
        
        total_amount+=totalAmt
        
        #------------------------        
        myString+=str(client_id)+','+str(client_name)+','+str(payment_mode)+','+str(shipment_no)+','+str(invoice_date)+','+str(invSl)+','+str(actual_total_tp)+','+str(vat_total_amount)+','+str(discount)+','+str(sp_discount)+','+str(totalAmt)+'\n'
        
        for j in range(len(returnList)):
            retDict=returnList[j]
            ret_invoice_sl=retDict['invoice_sl']
            
            if record.sl==ret_invoice_sl:               
               return_date=retDict['return_date']
               retSl=str(session.prefix_invoice)+'RET'+str(retDict['depot_id'])+'-'+str(retDict['sl'])
               ret_actual_total_tp=retDict['ret_actual_total_tp']
               ret_vat_total_amount=retDict['vat_total_amount']
               ret_discount=retDict['discount']
               ret_sp_discount=retDict['sp_discount']
               
               #------------------------        
               myString+=',,,,'+str(return_date)+','+str(retSl)+',('+str(ret_actual_total_tp)+'),('+str(ret_vat_total_amount)+'),('+str(ret_discount)+'),('+str(ret_sp_discount)+'),\n'
    
    myString+=str(invoiceTotal)+' Invoice(s),,,,,,,,,Total:,'+str(round(total_amount,2))+'\n'
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=5.1_download_synopsisRpt_SD_AD_AfterDelivery_withRetDet.csv'   
    return str(myString)
    


#Update invoice status as Post or Cancel
def post_invoice_bak():
    c_id=session.cid
    
    req_depot=request.vars.deptId
    req_sl=request.vars.slNo
    d_man_id=request.vars.deliveryManId
    req_date=request.vars.invoiceDate
    
    ym_date=str(req_date)[0:7]+'-01'
    
    existRow=db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==req_depot) & (db.sm_invoice_head.sl==req_sl)& (db.sm_invoice_head.status=='Submitted')).select(db.sm_invoice_head.id,db.sm_invoice_head.rep_id,db.sm_invoice_head.client_id,db.sm_invoice_head.discount,db.sm_invoice_head.acknowledge_flag,limitby=(0,1))
    if not existRow:
        return 'Error<fd>Required valid request'
    else:
        client_id=existRow[0].client_id
        discount=float(existRow[0].discount)
        acknowledge_flag=existRow[0].acknowledge_flag
        
        if acknowledge_flag==1:
            return 'Error<fd>Required Client Credit Acknowledgment'
        else:            
            batchIdrows=db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==req_depot) & (db.sm_invoice.sl==req_sl) & (db.sm_invoice.batch_id=='')).select(db.sm_invoice.id,limitby=(0,1))
            if batchIdrows:
                #session.flash = 'Required Batch ID for all Items'
                return 'Error<fd>Required Batch ID for all Items'
            else:
                d_man_name=''
                dmanRecords=db((db.sm_delivery_man.cid==c_id)& (db.sm_delivery_man.depot_id==req_depot) & (db.sm_delivery_man.d_man_id==d_man_id)).select(db.sm_delivery_man.id,db.sm_delivery_man.name,limitby=(0,1))
                if dmanRecords:
                    d_man_name=dmanRecords[0].name
                
                #----------------- INVOICE POST
                
                if req_depot=='' or req_sl=='' or req_date=='':
                    return 'Error<fd>Depot/SL/Date missing'
                else:        
                    if (ym_date=='' or ym_date==None):
                        return 'Error<fd>Invalid invoice date'
                    else:
                        #--------------------------------
                        resStr=''                
                        
                        totalAmount=0
                        total_tp_amount=0
                        total_vat_amount=0
                        
                        rows=db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==req_depot) & (db.sm_invoice.sl==req_sl) & (db.sm_invoice.status=='Submitted')).select(db.sm_invoice.quantity,db.sm_invoice.price,db.sm_invoice.item_vat,db.sm_invoice.discount)
                        for row in rows:
                            quantity=int(row.quantity)
                            price=float(row.price)
                            item_vat=float(row.item_vat)                        
                            
                            total_tp_amount+=round(quantity*price,6)
                            total_vat_amount+=round(quantity*item_vat,6)
                        
                        #-------------
                        totalAmount=round((round(total_tp_amount,2)+round(total_vat_amount,2)-round(discount,2)),2) #with vat
                        total_vat_amount=round(total_vat_amount,2)
                        
                        #Create string for balance return function                
                        if session.ledgerCreate=='YES':                    
                            strData=str(c_id)+'<fdfd>DELIVERY<fdfd>'+str(req_sl)+'<fdfd>'+str(datetime_fixed)+'<fdfd>'+str(req_depot)+'-'+str(req_sl)+'<fdfd>DPT-'+str(req_depot)+'<fdfd>CLT-'+str(client_id)+'<fdfd>'+str(totalAmount)
                            resStr=set_balance_transaction(strData)
                            resStrList=resStr.split('<sep>',resStr.count('<sep>'))
                            flag=resStrList[0]
                            msg=resStrList[1]
                        else:
                            flag='True'
                            msg='Success'
                            
                        if flag=='True':
                            #Update status of head and detail
                            session.flash=msg
                            db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==req_depot) & (db.sm_invoice.sl==req_sl)).update(status='Invoiced',d_man_id=d_man_id,d_man_name=d_man_name)
                            db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==req_depot) & (db.sm_invoice_head.sl==req_sl)).update(status='Invoiced',invoice_date=req_date,invoice_ym_date=ym_date,d_man_id=d_man_id,d_man_name=d_man_name,total_amount=totalAmount,vat_total_amount=total_vat_amount,empty_batch_flag=0)
                            
                            # call update depot stock (type,cid,depotid,sl)
                            update_depot_stock('DELIVERY',c_id,req_depot,req_sl)
                            
                        return 'Success'
                    

#========================= Show Invoice
def invoice_list_preview_bak():
    c_id=session.cid
    req_depot=session.depot_id
    
    #--------------- Title
    response.title='Preview Invoice'
    #-------------
    vslList=[]
    vslList=request.vars.vslList
    
    if vslList==None:
        session.flash='need select voucher'
        redirect('print_invoice')
    else:
        pass
    
    #-----------
    data_List=[]
    slList=[]
    for i in range(len(vslList)):
        req_sl=str(vslList[i]).strip()        
        if req_sl=='0':            
            continue
        
        slList.append(req_sl)
        
        #----------- 
        depot_id=''
        depot_name=''
        sl=0
        order_sl=0
        order_datetime=''
        delivery_date=''
        client_id=''
        client_name=''
        rep_id=''
        rep_name=''
        area_id=''
        area_name=''
        payment_mode=''
        discount=0
        note=''
        status=''
        
        records=db((db.sm_invoice.cid==c_id)& (db.sm_invoice.depot_id==req_depot) & (db.sm_invoice.sl==req_sl)).select(db.sm_invoice.ALL,orderby=db.sm_invoice.item_name)
        if records:        
            depot_id=records[0].depot_id
            depot_name=records[0].depot_name
            
            sl=records[0].sl
            
            order_sl=records[0].order_sl
            order_datetime=records[0].order_datetime
            delivery_date=records[0].delivery_date
            
            client_id=records[0].client_id
            client_name=records[0].client_name
            rep_id=records[0].rep_id
            rep_name=records[0].rep_name
            area_id=records[0].area_id
            area_name=records[0].area_name            
            payment_mode=records[0].payment_mode    
            discount=records[0].discount                     
            note=records[0].note
            status=records[0].status
            
            #--------------------
            vdDictList=[]
            for vdRow in records:        
                item_id=vdRow.item_id
                item_name=vdRow.item_name
                category_id=vdRow.category_id
                quantity=vdRow.quantity
                bonus_qty=vdRow.bonus_qty
                price=vdRow.price         
                short_note=vdRow.short_note
                
                #------------------------
                vdDict= {'item_id': item_id,'item_name': item_name,'category_id':category_id,'quantity': quantity,'bonus_qty':bonus_qty,'price': price,'short_note': short_note}
                vdDictList.append(vdDict)
        
            vhDict={'depot_id':depot_id,'depot_name':depot_name,'sl':sl,'order_sl':order_sl,'order_datetime':order_datetime,'delivery_date':delivery_date,'client_id':client_id,'client_name':client_name,
                    'rep_id':rep_id,'rep_name':rep_name,'area_id':area_id,'area_name':area_name,'status':status,'discount':discount,'note':note,'payment_mode':payment_mode,'vdList':vdDictList}
            data_List.append(vhDict)
    
    
    #------------------- print status (field2) update
    if len(slList)>0:
        db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==req_depot) & (db.sm_invoice_head.sl.belongs(slList))).update(field2=1)      

    #-------------------------
    return dict(data_List=data_List)





