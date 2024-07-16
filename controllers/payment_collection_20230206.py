
#======================= Receivable amount list for collection
def collection_list():
    c_id=session.cid
    
    #----------------    
    #Check access permission
    #----------Task assaign----------
    task_id='rm_client_payment_manage'
    access_permission=check_role(task_id)
    if (access_permission==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
        
    response.title='Payment Collection'
    
    #Set text for filter    
    btn_filter_payment=request.vars.btn_filter
    btn_all=request.vars.btn_all
    
    search_from_dt=str(request.vars.from_dt).strip()
    search_to_dt=str(request.vars.to_dt).strip()
    dp_id=str(request.vars.dp_id).strip()
    territory_id=str(request.vars.territory_id).strip()
    invoice_term=str(request.vars.invoice_term).strip()
    payment_old_inv_no=str(request.vars.payment_old_inv_no).strip()
    payment_customer_id=str(request.vars.payment_customer_id).strip()    
    payment_inv_sl=str(request.vars.payment_inv_sl).strip()
    
    reqPage=len(request.args)
    # Set sessions for filter
    if btn_filter_payment:
        session.btn_filter_payment=btn_filter_payment        
        session.dp_id=dp_id
        session.territory_id=territory_id
        session.invoice_term=invoice_term
        session.payment_customer_id=payment_customer_id
        session.payment_old_inv_no=payment_old_inv_no
        try:
            if payment_inv_sl!='':
                payment_inv_sl=int(payment_inv_sl)
                session.payment_inv_sl=payment_inv_sl            
        except:
            session.payment_inv_sl=''
            
        #---
        try:
            search_from_dt=datetime.datetime.strptime(search_from_dt,'%Y-%m-%d').strftime('%Y-%m-%d')
            session.search_from_dt=search_from_dt
        except:
            session.search_from_dt=''
            
        #---
        try:
            search_to_dt=datetime.datetime.strptime(search_to_dt,'%Y-%m-%d').strftime('%Y-%m-%d')
            session.search_to_dt=search_to_dt
        except:
            session.search_to_dt=''
            
        reqPage=0
        
    elif btn_all:
        session.btn_filter_payment=None
        session.dp_id=None
        session.territory_id=None
        session.invoice_term=None
        session.search_from_dt=None
        session.search_to_dt=''        
        session.payment_customer_id=None
        session.payment_inv_sl=None
        session.payment_old_inv_no=None
        reqPage=0
        
    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=150   #session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    
    limit1=page*items_per_page
    limit2=(page+1)*items_per_page+1
    
    #--------end paging  
    
    # Set query based on search type
    
    totalRecords=0
    condStr="cid='"+str(c_id)+"' and status='Invoiced' and inv_pending_flag=0 and round(round(total_amount,2)-round(round(return_tp,2)+round(return_vat,2)-round(return_discount,2),2),2)>round(collection_amount,2) "
    
    #qset=db()
    #qset=qset(db.sm_invoice_head.cid==c_id)
    #qset=qset(db.sm_invoice_head.status=='Invoiced')
    #qset=qset(db.sm_invoice_head.inv_pending_flag==0)   #used for not deliverd
    #qset=qset((db.sm_invoice_head.total_amount-(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat-db.sm_invoice_head.return_discount)) > db.sm_invoice_head.collection_amount)
    
    if (session.user_type!='Depot'):
        records=''
        response.flash='Only depot user can payment collect'
    else:
        #qset=qset(db.sm_invoice_head.depot_id==session.depot_id)        
        condStr+=" and depot_id='"+str(session.depot_id)+"'"
        
        if (session.btn_filter_payment):
            
            if (session.search_from_dt=='' or session.search_from_dt==None) and (not (session.search_to_dt=='' or session.search_to_dt==None)):
                #qset=qset(db.sm_invoice_head.invoice_date==session.search_to_dt)
                condStr+=" and invoice_date='"+str(session.search_to_dt)+"'"
            else:
                if not (session.search_from_dt=='' or session.search_from_dt==None):
                    #qset=qset(db.sm_invoice_head.invoice_date>=session.search_from_dt)
                    condStr+=" and invoice_date>='"+str(session.search_from_dt)+"'"
                    
                if not (session.search_to_dt=='' or session.search_to_dt==None):
                    #qset=qset(db.sm_invoice_head.invoice_date<=session.search_to_dt)
                    condStr+=" and invoice_date<='"+str(session.search_to_dt)+"'"
                    
            #------------
            if not (session.dp_id=='' or session.dp_id==None):
                dp_id=str(session.dp_id).split('|')[0]
                #qset=qset(db.sm_invoice_head.d_man_id==dp_id)
                condStr+=" and d_man_id='"+str(dp_id)+"'"
            #------------
            if not (session.territory_id=='' or session.territory_id==None):
                territory_id=str(session.territory_id).split('|')[0]
                #qset=qset(db.sm_invoice_head.area_id==territory_id)
                condStr+=" and area_id='"+str(territory_id)+"'"
            
            #------------
            if not (session.payment_customer_id=='' or session.payment_customer_id==None):
                payment_customer_id=str(session.payment_customer_id).split('|')[0]
                #qset=qset(db.sm_invoice_head.client_id==payment_customer_id)
                condStr+=" and client_id='"+str(payment_customer_id)+"'"
            #------------
            if not (session.payment_inv_sl=='' or session.payment_inv_sl==None):
                payment_inv_sl=session.payment_inv_sl
                #qset=qset(db.sm_invoice_head.sl==payment_inv_sl)
                condStr+=" and sl="+str(payment_inv_sl)+""
            
            if not (session.invoice_term=='' or session.invoice_term==None):
                invoice_term=str(session.invoice_term)
                #qset=qset(db.sm_invoice_head.payment_mode==invoice_term)
                condStr+=" and payment_mode='"+str(invoice_term)+"'"
                
            if not (session.payment_old_inv_no=='' or session.payment_old_inv_no==None):
                payment_old_inv_no=str(session.payment_old_inv_no).upper()
                #qset=qset(db.sm_invoice_head.note.upper().like('%'+payment_old_inv_no+'%'))
                condStr+=" and note like ('%"+str(payment_old_inv_no)+"%')"
                
    #records=qset.select(db.sm_invoice_head.ALL,orderby=~db.sm_invoice_head.sl|~db.sm_invoice_head.note,limitby=limitby)
    
    selectStr="select * from sm_invoice_head where ("+str(condStr)+") order by `sl` asc,`id` asc, `note` desc limit "+str(limit1)+","+str(limit2)
#     return selectStr
    recordsList=db.executesql(selectStr,as_dict = True)
    
    #totalRecords=qset.count()
    
    totalRecords=len(recordsList)
    
    #------------ filter form
    filterform =SQLFORM(db.sm_search_date,
                  fields=['from_dt','to_dt']
                  )
    
    if (session.search_from_dt=='' or session.search_from_dt==None):
        filterform.vars.from_dt=''
    else:
        filterform.vars.from_dt=session.search_from_dt
        
    if (session.search_to_dt==None):
        filterform.vars.to_dt=current_date
    else:
        filterform.vars.to_dt=session.search_to_dt
        
    if filterform.accepts(request.vars,session):
        pass
        
    invoiceTermRows=db((db.sm_category_type.cid==session.cid) & (db.sm_category_type.type_name=='PAYMENT_MODE')).select(db.sm_category_type.cat_type_id,orderby=db.sm_category_type.cat_type_id)
    paymentTypeRows=db((db.sm_category_type.cid==session.cid) & (db.sm_category_type.type_name=='PAYMENT_TYPE')).select(db.sm_category_type.cat_type_id,orderby=db.sm_category_type.cat_type_id)
    batchRows=db((db.sm_payment_collection.cid==session.cid) & (db.sm_payment_collection.depot_id==session.depot_id) & (db.sm_payment_collection.collection_date==current_date)&(db.sm_payment_collection.collection_batch!='')).select(db.sm_payment_collection.collection_batch,orderby=~db.sm_payment_collection.collection_batch,groupby=db.sm_payment_collection.collection_batch)
    
    #------------ filter form
    collectionform =SQLFORM(db.sm_search_date,
                  fields=['to_dt_2']
                  )
    
    return dict(recordsList=recordsList,batchRows=batchRows,filterform=filterform,collectionform=collectionform,totalRecords=totalRecords,invoiceTermRows=invoiceTermRows,paymentTypeRows=paymentTypeRows,page=page,items_per_page=items_per_page,access_permission=access_permission)
 
# =====================Submit to Post=============== 
# def collection_list_update_bak():
#     c_id=session.cid
#     depotId=session.depot_id
#
#     #--------------- Title
#     response.title='Preview Collection'
#     #-------------
#     vslList=[]
#     vslList=request.vars.vslList
#
#     if vslList==None:
#         session.flash='need select voucher'
#         redirect('collection_list')
#     else:
#         pass
#
#     payment_type=request.vars.payment_type
#     collectionNote=request.vars.notes
#     collectionBatch=request.vars.collectionBatch
#     paymentCollectionDate=request.vars.to_dt_2
#
#     try:
#         payment_collection_date=datetime.datetime.strptime(str(paymentCollectionDate),'%Y-%m-%d').strftime('%Y-%m-%d')
#     except:
#         payment_collection_date=current_date
#
#     payment_ym_date=str(payment_collection_date)[0:7] + '-01'
#
#     if payment_type=='':
#         session.flash='Required Payment Type'
#         redirect('collection_list')
#     else:
#         pass
#
#     if collectionBatch=='' or collectionBatch==None:
#         collectionBatch=str(date_fixed)[0:16].replace('-','').replace(':','').replace(' ','-')+str(date_fixed.strftime('%p'))
#
#         newExist=db((db.sm_payment_collection.cid==c_id)& (db.sm_payment_collection.depot_id==session.depot_id) &(db.sm_payment_collection.collection_date==current_date) &(db.sm_payment_collection.collection_batch==collectionBatch)).select(db.sm_payment_collection.id,limitby=(0,1))
#         if newExist:
#             session.flash='Batch No error, please try again after 1 minute'
#             redirect('collection_list')
#
#         session.lastCollectionBatch=None
#     else:
#         session.lastCollectionBatch=collectionBatch
#
#     collection_batch=collectionBatch
#     collection_note=collectionNote
#     receipt_description=''
#
#     #-----------
#     data_List=[]
#     slList=[]
#     totalCollectedAmt=0
#     errorFlag=False
#     errorMsg=''
#
#     slStrShow=''
#     slStrShowList=[]
#     paymentDict={}
#     pamentInsertList=[]
#     rowidList=[]
#     for i in range(len(vslList)):
#         rowId=str(vslList[i]).strip()
#         if rowId=='-1' or rowId=='-':
#             continue
#
#         varName='appliedAmount_'+rowId
#         appliedAmount=str(request.vars[varName]).replace(',', '')
#
#         if appliedAmount==None:
#             continue
#
#         try:
#             appliedAmount=float(appliedAmount)
#             if appliedAmount<0:
#                 appliedAmount=0
#
#         except:
#             appliedAmount=0
#
#         if appliedAmount==0:
#             errorMsg='Invalid Applied Amount of Ref.'+rowId
#             errorFlag=True
#             break
#         else:
#             pass
#
#         slList.append(rowId)
#
#         #-----------
#         existRow=db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==depotId) & (db.sm_invoice_head.id==rowId) & (db.sm_invoice_head.field1!='InPrcess')).select(db.sm_invoice_head.ALL,limitby=(0,1))
#         if not existRow:
#             errorMsg='Invalid Ref.'+rowId
#             errorFlag=True
#             break
#         else:
#             slNo=existRow[0].sl
#             depot_name=existRow[0].depot_name
#             store_id=existRow[0].store_id
#             store_name=existRow[0].store_name
#             order_sl=existRow[0].order_sl
#             order_datetime=existRow[0].order_datetime
#             delivery_date=existRow[0].delivery_date
#             payment_mode=existRow[0].payment_mode
#             credit_note=existRow[0].credit_note
#             rep_id=existRow[0].rep_id
#             rep_name=existRow[0].rep_name
#             d_man_id=existRow[0].d_man_id
#             d_man_name=existRow[0].d_man_name
#             area_id=existRow[0].area_id
#             area_name=existRow[0].area_name
#             level0_id=existRow[0].level0_id
#             level0_name=existRow[0].level0_name
#             level1_id=existRow[0].level1_id
#             level1_name=existRow[0].level1_name
#             level2_id=existRow[0].level2_id
#             level2_name=existRow[0].level2_name
#             level3_id=existRow[0].level3_id
#             level3_name=existRow[0].level3_name
#             invoice_date=existRow[0].invoice_date
#             invoice_ym_date=existRow[0].invoice_ym_date
#             market_id=existRow[0].market_id
#             market_name=existRow[0].market_name
#
#             shipment_no=existRow[0].shipment_no
#
#             cl_category_id=existRow[0].cl_category_id
#             cl_category_name=existRow[0].cl_category_name
#             cl_sub_category_id=existRow[0].cl_sub_category_id
#             cl_sub_category_name=existRow[0].cl_sub_category_name
#             special_territory_code=existRow[0].special_territory_code
#             client_limit_amt=existRow[0].client_limit_amt
#
#             doc_number=''
#
#             collection_date=current_date
#             ym_date=str(collection_date)[0:7] + '-01'
#
#             client_id=existRow[0].client_id
#             client_name=existRow[0].client_name
#             total_amount=round(existRow[0].total_amount,2)
#             collection_amount=round(existRow[0].collection_amount,2)
#
#             actual_total_tp=round(existRow[0].actual_total_tp,2)
#             vat_total_amount=round(existRow[0].vat_total_amount,2)
#             discount=round(existRow[0].discount,2)
#             sp_discount=round(existRow[0].sp_discount,2)
#
#             return_tp=float(existRow[0].return_tp)
#             return_vat=float(existRow[0].return_vat)
#             return_discount=float(existRow[0].return_discount)
#
#             returnAmount=round(round(return_tp,2)+round(return_vat,2)-round(return_discount,2),2)
#
#             receivable_amount=round(total_amount-returnAmount-collection_amount,2)
#             appliedAmount=round(appliedAmount,2)
#             totalCollectAmount=round(collection_amount+appliedAmount,2)
#
#             currentReceivable=round(total_amount-returnAmount,2)
#
#             if float(totalCollectAmount) > float(currentReceivable):
#                 errorMsg='Applied amount can not be greater than due amount. Ref.'+rowId+','+str(totalCollectAmount)+':'+str(currentReceivable)
#                 errorFlag=True
#                 break
#             else:
#                 #--------------------------------
#                 resStr=''
#                 paymentDict={'cid':c_id,'depot_id':depotId,'depot_name':depot_name,'sl':slNo,'head_rowid':rowId,'store_id':store_id,'store_name':store_name,'order_sl':order_sl,'order_datetime':order_datetime,'delivery_date':delivery_date,'payment_mode':payment_mode,'credit_note':credit_note,'payment_type':payment_type,'client_id':client_id,'client_name':client_name,'rep_id':rep_id,'rep_name':rep_name,'market_id':market_id,
#                              'market_name':market_name,'d_man_id':d_man_id,'d_man_name':d_man_name,'area_id':area_id,'area_name':area_name,'level0_id':level0_id,'level0_name':level0_name,'level1_id':level1_id,'level1_name':level1_name,'level2_id':level2_id,'level2_name':level2_name,'level3_id':level3_id,'level3_name':level3_name,'cl_category_id':cl_category_id,'cl_category_name':cl_category_name,'cl_sub_category_id':cl_sub_category_id,
#                              'cl_sub_category_name':cl_sub_category_name,'special_territory_code':special_territory_code,'invoice_date':invoice_date,'invoice_ym_date':invoice_ym_date,'collection_date':collection_date,'ym_date':ym_date,'payment_collection_date':payment_collection_date,'payment_ym_date':payment_ym_date,'collection_batch':collection_batch,'collection_note':collection_note,'shipment_no':shipment_no,'doc_number':doc_number,
#                              'receipt_description':receipt_description,'transaction_type':'Payment','collection_flag':'1','total_inv_amount':total_amount,'receivable_amount':receivable_amount,'collection_amount':appliedAmount,'status':'Inprocess','rpt_trans_flag':'1'}
#
#                 pamentInsertList.append(paymentDict)
#                 rowidList.append(rowId)
#                 totalCollectedAmt+=appliedAmount
#
#
#             doc_number=''
#             if float(totalCollectAmount) > float(currentReceivable):
#                 errorMsg='Applied amount can not be greater than due amount. Ref.'+rowId+','+str(totalCollectAmount)+':'+str(currentReceivable)
#                 errorFlag=True
#                 break
#             else:
#                 #--------------------------------
# #                 slStrShowList.append(idNo)
#                 resStr=''
#
#
#
#
# #     return errorFlag
#     if errorFlag==True:
#         session.flash=errorMsg+'. And Collected Tk.'+str(totalCollectedAmt)
#         redirect (URL('collection_list'))
#     else:
# #         return totalCollectedAmt
#         if len(pamentInsertList) > 0:
#             inCountList=db.sm_payment_collection.bulk_insert(pamentInsertList)
#             db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.id.belongs(rowidList))).update(field1='1')
#
#         session.flash='Successfully In Process TK. '+str(totalCollectedAmt)
#         redirect (URL('collection_list'))
#
#     #-------------------------
#     return ''
#
# # ==========================Cron======================
# def collection_list_update_cron():
#     c_id=session.cid
#     depotId=session.depot_id
#
#     #--------------- Title
#     response.title='Preview Collection'
#     #-------------
#
#
# #     Select from payment collection table===================
#     Pay_colRow=db((db.sm_payment_collection.cid==c_id)& (db.sm_payment_collection.status=='Inprocess') ).select(db.sm_payment_collection.ALL,limitby=(0,20))
#
# #     ==================================================
#     for  Pay_colRow in Pay_colRow:
#         errorFlag=False
#         c_id=Pay_colRow.cid
#         depotId=Pay_colRow.depot_id
#         payment_type=Pay_colRow.payment_type
#         collectionNote=Pay_colRow.collection_note
#         collectionBatch=Pay_colRow.collection_batch
#         paymentCollectionDate=Pay_colRow.collection_date
#         rowId=Pay_colRow.head_rowid
#         appliedAmount=Pay_colRow.collection_amount
#         mrNo=rowId
#         pc_rowID=Pay_colRow.id
#         try:
#             payment_collection_date=datetime.datetime.strptime(str(paymentCollectionDate),'%Y-%m-%d').strftime('%Y-%m-%d')
#         except:
#             payment_collection_date=current_date
#
#             payment_ym_date=str(payment_collection_date)[0:7] + '-01'
#
#
#
#         if collectionBatch=='' or collectionBatch==None:
#             collectionBatch=str(date_fixed)[0:16].replace('-','').replace(':','').replace(' ','-')+str(date_fixed.strftime('%p'))
#
#         newExist=db((db.sm_payment_collection.cid==c_id)& (db.sm_payment_collection.depot_id==session.depot_id) &(db.sm_payment_collection.collection_date==current_date) &(db.sm_payment_collection.collection_batch==collectionBatch)).select(db.sm_payment_collection.id,limitby=(0,1))
#         if newExist:
#             pass
# #             session.flash='Batch No error, please try again after 1 minute'
# #             redirect('collection_list')
# #
# #         session.lastCollectionBatch=None
#         else:
#             session.lastCollectionBatch=collectionBatch
#
#             collection_batch=collectionBatch
#             collection_note=collectionNote
#             receipt_description=''
#
#     #-----------
# #             data_List=[]
# #             slList=[]
# #             totalCollectedAmt=0
#             errorFlag=False
#             errorMsg=''
# #             for i in range(len(vslList)):
# #                 rowId=str(vslList[i]).strip()
# #                 if rowId=='-1' or rowId=='-':
# #                     continue
#
# #             varName='appliedAmount_'+rowId
# #             appliedAmount=str(request.vars[varName]).replace(',', '')
#
#             if appliedAmount==None:
#                 continue
#
#             try:
#                 appliedAmount=float(appliedAmount)
#                 if appliedAmount<0:
#                     appliedAmount=0
#
#             except:
#                 appliedAmount=0
#
#             if appliedAmount==0:
#                 errorMsg='Invalid Applied Amount of Ref.'+rowId
#                 errorFlag=True
#                 break
#             else:
#                 pass
#
# #             return 'asasa'
#
#         #-----------
#         existRow=db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==depotId) & (db.sm_invoice_head.id==rowId)).select(db.sm_invoice_head.ALL,limitby=(0,1))
# #             return existRow
#         if not existRow:
#             errorMsg='Invalid Ref.'+rowId
#             errorFlag=True
#             break
#         else:
#             slNo=existRow[0].sl
#             depot_name=existRow[0].depot_name
#             store_id=existRow[0].store_id
#             store_name=existRow[0].store_name
#             order_sl=existRow[0].order_sl
#             order_datetime=existRow[0].order_datetime
#             delivery_date=existRow[0].delivery_date
#             payment_mode=existRow[0].payment_mode
#             credit_note=existRow[0].credit_note
#             rep_id=existRow[0].rep_id
#             rep_name=existRow[0].rep_name
#             d_man_id=existRow[0].d_man_id
#             d_man_name=existRow[0].d_man_name
#             area_id=existRow[0].area_id
#             area_name=existRow[0].area_name
#             level0_id=existRow[0].level0_id
#             level0_name=existRow[0].level0_name
#             level1_id=existRow[0].level1_id
#             level1_name=existRow[0].level1_name
#             level2_id=existRow[0].level2_id
#             level2_name=existRow[0].level2_name
#             level3_id=existRow[0].level3_id
#             level3_name=existRow[0].level3_name
#             invoice_date=existRow[0].invoice_date
#             invoice_ym_date=existRow[0].invoice_ym_date
#             market_id=existRow[0].market_id
#             market_name=existRow[0].market_name
#
#             shipment_no=existRow[0].shipment_no
#
#             cl_category_id=existRow[0].cl_category_id
#             cl_category_name=existRow[0].cl_category_name
#             cl_sub_category_id=existRow[0].cl_sub_category_id
#             cl_sub_category_name=existRow[0].cl_sub_category_name
#             special_territory_code=existRow[0].special_territory_code
#             client_limit_amt=existRow[0].client_limit_amt
#
#             doc_number=''
#
#             collection_date=current_date
#             ym_date=str(collection_date)[0:7] + '-01'
#
#             client_id=existRow[0].client_id
#             client_name=existRow[0].client_name
#             total_amount=round(existRow[0].total_amount,2)
#             collection_amount=round(existRow[0].collection_amount,2)
#
#
#             actual_total_tp=round(existRow[0].actual_total_tp,2)
#             vat_total_amount=round(existRow[0].vat_total_amount,2)
#             discount=round(existRow[0].discount,2)
#             sp_discount=round(existRow[0].sp_discount,2)
#
#             return_tp=float(existRow[0].return_tp)
#             return_vat=float(existRow[0].return_vat)
#             return_discount=float(existRow[0].return_discount)
#
#             returnAmount=round(round(return_tp,2)+round(return_vat,2)-round(return_discount,2),2)
#
#             receivable_amount=round(total_amount-returnAmount-collection_amount,2)
#             appliedAmount=round(appliedAmount,2)
#             totalCollectAmount=round(collection_amount+appliedAmount,2)
#
#             currentReceivable=round(total_amount-returnAmount,2)
# #                 return appliedAmount
#             if float(totalCollectAmount) > float(currentReceivable):
#                 errorMsg='Applied amount can not be greater than due amount. Ref.'+str(rowId)+','+str(totalCollectAmount)+':'+str(currentReceivable)
#                 errorFlag=True
#                 break
#             else:
#                 #--------------------------------
#                 resStr=''
#
#                 if session.ledgerCreate=='YES':
#                     strData=str(c_id)+'<fdfd>CLTPAYMENT<fdfd>'+str(slNo)+'<fdfd>'+str(datetime_fixed)+'<fdfd>'+str(depotId)+'-'+str(slNo)+'<fdfd>CLT-'+str(client_id)+'<fdfd>DPT-'+str(depotId)+'<fdfd>'+str(appliedAmount)
#                     resStr=set_balance_transaction(strData)
#                     resStrList=resStr.split('<sep>',resStr.count('<sep>'))
#                     flag=resStrList[0]
#                     msg=resStrList[1]
#                 else:
#                     flag='True'
#                     msg='Success'
#
#
#                     #----------------------- Report Transaction ***
# #                 return flag
#                 if flag=='True':
#
#                     try:
#                         collectonTp=round(actual_total_tp/total_amount*appliedAmount,2)
#                         collectonVat=round(vat_total_amount/total_amount*appliedAmount,2)
#                         collectonDisc=round(discount/total_amount*appliedAmount,2)
#                         collectonSpDisc=round(sp_discount/total_amount*appliedAmount,2)
#                     except:
#                         collectonTp=0
#                         collectonVat=0
#                         collectonDisc=0
#                         collectonSpDisc=0
#
#                     transaction_date=collection_date
#                     db.sm_rpt_transaction.insert(cid=c_id,depot_id=depotId,depot_name=depot_name,store_id=store_id,store_name=store_name,inv_rowid=rowId,inv_sl=slNo,invoice_date=invoice_date,transaction_type='PAYCOLL',transaction_date=transaction_date,transaction_ref=mrNo,transaction_ref_date=payment_collection_date,trans_net_amt=appliedAmount*(-1),tp_amt=collectonTp*(-1),vat_amt=collectonVat*(-1),disc_amt=collectonDisc*(-1),spdisc_amt=collectonSpDisc*(-1),adjust_amount=0,
#                                              delivery_date=delivery_date,payment_mode=payment_mode,credit_note=credit_note,client_id=client_id,client_name=client_name,cl_category_id=cl_category_id,cl_category_name=cl_category_name,cl_sub_category_id=cl_sub_category_id,cl_sub_category_name=cl_sub_category_name,client_limit_amt=client_limit_amt,
#                                              rep_id=rep_id,rep_name=rep_name,market_id=market_id,market_name=market_name,d_man_id=d_man_id,d_man_name=d_man_name,level0_id=level0_id,level0_name=level0_name,level1_id=level1_id,level1_name=level1_name,level2_id=level2_id,level2_name=level2_name,area_id=area_id,area_name=area_name,shipment_no=shipment_no,note=collectionNote)
#                     #------------------
#
#                     #Update status of head and detail
#                     #session.flash=msg
#                     db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==depotId) & (db.sm_invoice_head.id==rowId)).update(collection_amount=totalCollectAmount)
#                     db((db.sm_payment_collection.cid==c_id)& (db.sm_payment_collection.id==pc_rowID)).update(status='Posted')
#
# #                         totalCollectedAmt+=appliedAmount
#                     #session.flash='Successfully collected TK. '+str(appliedAmount)+'/= From '+str(client_id)+'-'+str(client_name)
#                 else:
#                     errorMsg='Process failed. Ref.'+rowId
#                     errorFlag=True
#                     break
#
#         if errorFlag==True:
#             session.flash=errorMsg+'. And Collected Tk.'+str(appliedAmount)
#             redirect (URL('collection_list'))
#         else:
#             session.flash='Successfully collected TK. '+str(appliedAmount)
#             redirect (URL('collection_list'))
#
#     #-------------------------
#     return ''
# # ==========================Submit to Post================
    
#========================= Payment collect single/multi
def collection_list_update():
    c_id=session.cid
    depotId=session.depot_id
    
    #--------------- Title
    response.title='Preview Collection'
    #-------------
    vslList=[]
    vslList=request.vars.vslList
    
    if vslList==None:
        session.flash='need select voucher'
        redirect('collection_list')
    else:
        pass
        
    payment_type=request.vars.payment_type
    collectionNote=request.vars.notes
    collectionBatch=request.vars.collectionBatch
    paymentCollectionDate=request.vars.to_dt_2
    
    try:
        payment_collection_date=datetime.datetime.strptime(str(paymentCollectionDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        payment_collection_date=current_date
        
    payment_ym_date=str(payment_collection_date)[0:7] + '-01'
    
    if payment_type=='':
        session.flash='Required Payment Type'
        redirect('collection_list')
    else:
        pass
        
    if collectionBatch=='' or collectionBatch==None:
        collectionBatch=str(date_fixed)[0:16].replace('-','').replace(':','').replace(' ','-')+str(date_fixed.strftime('%p'))
        
        newExist=db((db.sm_payment_collection.cid==c_id)& (db.sm_payment_collection.depot_id==session.depot_id) &(db.sm_payment_collection.collection_date==current_date) &(db.sm_payment_collection.collection_batch==collectionBatch)).select(db.sm_payment_collection.id,limitby=(0,1))
        if newExist:
            session.flash='Batch No error, please try again after 1 minute'
            redirect('collection_list')
        
        session.lastCollectionBatch=None
    else:
        session.lastCollectionBatch=collectionBatch
        
    collection_batch=collectionBatch
    collection_note=collectionNote    
    receipt_description=''   
    
    #-----------
    data_List=[]
    slList=[]
    totalCollectedAmt=0
    errorFlag=False
    errorMsg=''
    for i in range(len(vslList)):
        rowId=str(vslList[i]).strip()        
        if rowId=='-1' or rowId=='-':            
            continue
            
        varName='appliedAmount_'+rowId
        appliedAmount=str(request.vars[varName]).replace(',', '')
        
        if appliedAmount==None:
            continue
            
        try:
            appliedAmount=float(appliedAmount)
            if appliedAmount<0:
                appliedAmount=0
                
        except:
            appliedAmount=0
    
        if appliedAmount==0:            
            errorMsg='Invalid Applied Amount of Ref.'+rowId
            errorFlag=True
            break
        else:
            pass
        
        slList.append(rowId)
        
        #-----------
        existRow=db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==depotId) & (db.sm_invoice_head.id==rowId)).select(db.sm_invoice_head.ALL,limitby=(0,1))
        if not existRow:            
            errorMsg='Invalid Ref.'+rowId
            errorFlag=True
            break
        else:
            slNo=existRow[0].sl
            depot_name=existRow[0].depot_name
            store_id=existRow[0].store_id
            store_name=existRow[0].store_name
            order_sl=existRow[0].order_sl
            order_datetime=existRow[0].order_datetime
            delivery_date=existRow[0].delivery_date
            payment_mode=existRow[0].payment_mode
            credit_note=existRow[0].credit_note
            rep_id=existRow[0].rep_id
            rep_name=existRow[0].rep_name
            d_man_id=existRow[0].d_man_id
            d_man_name=existRow[0].d_man_name
            area_id=existRow[0].area_id
            area_name=existRow[0].area_name
            level0_id=existRow[0].level0_id
            level0_name=existRow[0].level0_name
            level1_id=existRow[0].level1_id
            level1_name=existRow[0].level1_name
            level2_id=existRow[0].level2_id
            level2_name=existRow[0].level2_name
            level3_id=existRow[0].level3_id
            level3_name=existRow[0].level3_name
            invoice_date=existRow[0].invoice_date
            invoice_ym_date=existRow[0].invoice_ym_date
            market_id=existRow[0].market_id
            market_name=existRow[0].market_name
            
            shipment_no=existRow[0].shipment_no
            
            cl_category_id=existRow[0].cl_category_id
            cl_category_name=existRow[0].cl_category_name
            cl_sub_category_id=existRow[0].cl_sub_category_id
            cl_sub_category_name=existRow[0].cl_sub_category_name
            special_territory_code=existRow[0].special_territory_code
            client_limit_amt=existRow[0].client_limit_amt
            
            doc_number=''
            
            collection_date=current_date
            ym_date=str(collection_date)[0:7] + '-01'
            
            client_id=existRow[0].client_id
            client_name=existRow[0].client_name
            total_amount=round(existRow[0].total_amount,2)
            collection_amount=round(existRow[0].collection_amount,2)
            
            actual_total_tp=round(existRow[0].actual_total_tp,2)
            vat_total_amount=round(existRow[0].vat_total_amount,2)
            discount=round(existRow[0].discount,2)
            sp_discount=round(existRow[0].sp_discount,2)
            
            return_tp=float(existRow[0].return_tp)
            return_vat=float(existRow[0].return_vat)
            return_discount=float(existRow[0].return_discount)
            
            returnAmount=round(round(return_tp,2)+round(return_vat,2)-round(return_discount,2),2)
            
            receivable_amount=round(total_amount-returnAmount-collection_amount,2)
            appliedAmount=round(appliedAmount,2)            
            totalCollectAmount=round(collection_amount+appliedAmount,2)
                   
            currentReceivable=round(total_amount-returnAmount,2)
            
            if float(totalCollectAmount) > float(currentReceivable):
                errorMsg='Applied amount can not be greater than due amount. Ref.'+rowId+','+str(totalCollectAmount)+':'+str(currentReceivable)
                errorFlag=True
                break
            else:
                #--------------------------------
                resStr=''                
                
                if session.ledgerCreate=='YES':
                    strData=str(c_id)+'<fdfd>CLTPAYMENT<fdfd>'+str(slNo)+'<fdfd>'+str(datetime_fixed)+'<fdfd>'+str(depotId)+'-'+str(slNo)+'<fdfd>CLT-'+str(client_id)+'<fdfd>DPT-'+str(depotId)+'<fdfd>'+str(appliedAmount)
                    resStr=set_balance_transaction(strData) 
                    resStrList=resStr.split('<sep>',resStr.count('<sep>'))
                    flag=resStrList[0]
                    msg=resStrList[1]
                else:
                    flag='True'
                    msg='Success'
                    
                if flag=='True':
                    insertRes=db.sm_payment_collection.insert(cid=c_id,depot_id=depotId,depot_name=depot_name,sl=slNo,head_rowid=rowId,store_id=store_id,store_name=store_name,order_sl=order_sl,order_datetime=order_datetime,delivery_date=delivery_date,payment_mode=payment_mode,credit_note=credit_note,payment_type=payment_type,client_id=client_id,client_name=client_name,rep_id=rep_id,
                                                    rep_name=rep_name,market_id=market_id,market_name=market_name,d_man_id=d_man_id,d_man_name=d_man_name,area_id=area_id,area_name=area_name,level0_id=level0_id,level0_name=level0_name,level1_id=level1_id,level1_name=level1_name,level2_id=level2_id,level2_name=level2_name,level3_id=level3_id,level3_name=level3_name,cl_category_id=cl_category_id,cl_category_name=cl_category_name,cl_sub_category_id=cl_sub_category_id,cl_sub_category_name=cl_sub_category_name,special_territory_code=special_territory_code,invoice_date=invoice_date,
                                                    invoice_ym_date=invoice_ym_date,collection_date=collection_date,ym_date=ym_date,payment_collection_date=payment_collection_date,payment_ym_date=payment_ym_date,collection_batch=collection_batch,collection_note=collection_note,shipment_no=shipment_no,doc_number=doc_number,receipt_description=receipt_description,transaction_type='Payment',collection_flag=1,total_inv_amount=total_amount,receivable_amount=receivable_amount,collection_amount=appliedAmount,status='Posted',rpt_trans_flag=1)
                    
                    mrNo = db.sm_payment_collection(insertRes).id
                    
                    #----------------------- Report Transaction ***
                    try:
                        collectonTp=round(actual_total_tp/total_amount*appliedAmount,2)
                        collectonVat=round(vat_total_amount/total_amount*appliedAmount,2)
                        collectonDisc=round(discount/total_amount*appliedAmount,2)
                        collectonSpDisc=round(sp_discount/total_amount*appliedAmount,2)
                    except:
                        collectonTp=0
                        collectonVat=0
                        collectonDisc=0
                        collectonSpDisc=0
                        
                    transaction_date=collection_date
                    db.sm_rpt_transaction.insert(cid=c_id,depot_id=depotId,depot_name=depot_name,store_id=store_id,store_name=store_name,inv_rowid=rowId,inv_sl=slNo,invoice_date=invoice_date,transaction_type='PAYCOLL',transaction_date=transaction_date,transaction_ref=mrNo,transaction_ref_date=payment_collection_date,trans_net_amt=appliedAmount*(-1),tp_amt=collectonTp*(-1),vat_amt=collectonVat*(-1),disc_amt=collectonDisc*(-1),spdisc_amt=collectonSpDisc*(-1),adjust_amount=0,
                                             delivery_date=delivery_date,payment_mode=payment_mode,credit_note=credit_note,client_id=client_id,client_name=client_name,cl_category_id=cl_category_id,cl_category_name=cl_category_name,cl_sub_category_id=cl_sub_category_id,cl_sub_category_name=cl_sub_category_name,client_limit_amt=client_limit_amt,
                                             rep_id=rep_id,rep_name=rep_name,market_id=market_id,market_name=market_name,d_man_id=d_man_id,d_man_name=d_man_name,level0_id=level0_id,level0_name=level0_name,level1_id=level1_id,level1_name=level1_name,level2_id=level2_id,level2_name=level2_name,area_id=area_id,area_name=area_name,shipment_no=shipment_no,note=collection_note)
                    #------------------
                    
                    #Update status of head and detail
                    #session.flash=msg
                    db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==depotId) & (db.sm_invoice_head.id==rowId)).update(collection_amount=totalCollectAmount)
                                        
                    totalCollectedAmt+=appliedAmount
                    #session.flash='Successfully collected TK. '+str(appliedAmount)+'/= From '+str(client_id)+'-'+str(client_name)
                else:
                    errorMsg='Process failed. Ref.'+rowId
                    errorFlag=True
                    break
                    
    if errorFlag==True:
        session.flash=errorMsg+'. And Collected Tk.'+str(totalCollectedAmt)
        redirect (URL('collection_list'))
    else:
        session.flash='Successfully collected TK. '+str(totalCollectedAmt)
        redirect (URL('collection_list'))
        
    #-------------------------
    return ''
    
#======================= collection_adjustment; reverse(negative=collection+)/adjustment(positive=collection-)
def collection_adjustment():
    task_id='rm_client_payment_manage'
    access_permission=check_role(task_id)
    if (access_permission==False or session.user_type!='Depot'):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    
    response.title='Collection Adjustment'
    
    c_id=session.cid
    
    #----------- Cause List    
    causeRows=db((db.sm_category_type.cid==session.cid)&(db.sm_category_type.type_name=='PAYMENT_ADJUSTMENT_TYPE')).select(db.sm_category_type.ALL,orderby=db.sm_category_type.id)
    
    #--------------
    btn_submit=request.vars.btn_submit    
    if btn_submit:
        depotId=request.vars.depot_id_value
        transaction_type=request.vars.transaction_type
        transaction_cause=request.vars.transaction_cause
        collection_flag=0
        
        try:
            inv_sl=int(request.vars.inv_sl)
            if inv_sl<0:
                inv_sl=0            
        except:
            inv_sl=0
        
        try:
            inv_rowid=int(request.vars.inv_rowid)
            if inv_rowid<0:
                inv_rowid=0
        except:
            inv_rowid=0
            
        client_id=str(request.vars.client_id).strip().split('|')[0]
        try:
            applied_amount=float(str(request.vars.applied_amount).replace(',', ''))
            if applied_amount<0:
                applied_amount=0
        except:
            applied_amount=0            
        try:
            confirm_amount=float(str(request.vars.confirm_amount).replace(',', ''))
        except:
            confirm_amount=0
            
        notes=request.vars.notes
        
        if (transaction_type=='' or transaction_cause==''  or client_id=='' or applied_amount=='' or confirm_amount==''):
            response.flash='Required all value'
        else:
            if inv_sl==0 and inv_rowid==0:
                response.flash='Required valid SL/Ref'
            else:
                if (applied_amount==0 or confirm_amount==0):
                    response.flash='Required valid amount'
                else:
                    if applied_amount!=confirm_amount:
                        response.flash='Amount and Confirm Amount need same'
                    else:
                        if transaction_cause=='COLLECTION ERROR' or transaction_cause=='ENTRY ERROR':
                            collection_flag=1
                            
                        #--------------
                        if inv_sl>0:        
                            existRow=db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==depotId) & (db.sm_invoice_head.sl==inv_sl) & (db.sm_invoice_head.client_id==client_id)).select(db.sm_invoice_head.ALL,limitby=(0,1))
                        else:
                            existRow=db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==depotId) & (db.sm_invoice_head.id==inv_rowid) & (db.sm_invoice_head.client_id==client_id)).select(db.sm_invoice_head.ALL,limitby=(0,1))
                            
                        if not existRow:
                            response.flash='Invalid invoice SL/Reference'                        
                        else:
                            inv_rowid=existRow[0].id
                            slNo=existRow[0].sl
                            depot_name=existRow[0].depot_name
                            store_id=existRow[0].store_id
                            store_name=existRow[0].store_name
                            order_sl=existRow[0].order_sl
                            order_datetime=existRow[0].order_datetime
                            delivery_date=existRow[0].delivery_date
                            payment_mode=existRow[0].payment_mode
                            credit_note=existRow[0].credit_note
                            rep_id=existRow[0].rep_id
                            rep_name=existRow[0].rep_name
                            d_man_id=existRow[0].d_man_id
                            d_man_name=existRow[0].d_man_name
                            area_id=existRow[0].area_id
                            area_name=existRow[0].area_name
                            level0_id=existRow[0].level0_id
                            level0_name=existRow[0].level0_name
                            level1_id=existRow[0].level1_id
                            level1_name=existRow[0].level1_name
                            level2_id=existRow[0].level2_id
                            level2_name=existRow[0].level2_name
                            level3_id=existRow[0].level3_id
                            level3_name=existRow[0].level3_name
                            invoice_date=existRow[0].invoice_date
                            invoice_ym_date=existRow[0].invoice_ym_date                            
                            market_id=existRow[0].market_id
                            market_name=existRow[0].market_name                            
                            shipment_no=existRow[0].shipment_no
                            
                            cl_category_id=existRow[0].cl_category_id
                            cl_category_name=existRow[0].cl_category_name
                            cl_sub_category_id=existRow[0].cl_sub_category_id
                            cl_sub_category_name=existRow[0].cl_sub_category_name
                            special_territory_code=existRow[0].special_territory_code
                            client_limit_amt=existRow[0].client_limit_amt
                            
                            collection_batch=''
                            collection_note=notes
                            
                            doc_number=''
                            receipt_description=''
                            applied_date=current_date
                            ym_date=str(applied_date)[0:7] + '-01'
                            
                            client_id=existRow[0].client_id
                            client_name=existRow[0].client_name
                            total_amount=float(existRow[0].total_amount)
                            collection_amount=float(existRow[0].collection_amount)
                            adjust_amount=float(existRow[0].adjust_amount)
                            
                            actual_total_tp=round(existRow[0].actual_total_tp,2)
                            vat_total_amount=round(existRow[0].vat_total_amount,2)
                            discount=round(existRow[0].discount,2)
                            sp_discount=round(existRow[0].sp_discount,2)
                            
                            return_tp=float(existRow[0].return_tp)
                            return_vat=float(existRow[0].return_vat)
                            return_discount=float(existRow[0].return_discount)                        
                            returnAmount=round(float(return_tp+return_vat-return_discount),2)                        
                            receivable_amount=round(total_amount-returnAmount-collection_amount,2)
                            
                            collection_amount=round(collection_amount,2)
                            adjust_amount=round(adjust_amount,2)                            
                            applied_amount=round(applied_amount,2)
                            
                            if transaction_type=='Negative':                   
                                reverse_amount=applied_amount*(-1)
                                
                                if applied_amount > collection_amount:
                                    response.flash='Decrease (Reverse) amount can be maximum Tk. '+str(collection_amount)                        
                                else:                                    
                                    totalCollectAmount=round(collection_amount-applied_amount,2)
                                    totalAdjustAmount=adjust_amount
                                    transaction_adjust_amount=0
                                    
                                    if collection_flag==0:
                                        totalAdjustAmount=round(adjust_amount-applied_amount,2)
                                        transaction_adjust_amount=applied_amount
                                        
                                    #--------------------------------
                                    resStr=''                
                                    
                                    if session.ledgerCreate=='YES':
                                        strData=str(c_id)+'<fdfd>PAYMENTCLT<fdfd>'+str(slNo)+'<fdfd>'+str(datetime_fixed)+'<fdfd>'+str(depotId)+'-'+str(slNo)+'<fdfd>DPT-'+str(depotId)+'<fdfd>CLT-'+str(client_id)+'<fdfd>'+str(applied_amount)
                                        resStr=set_balance_transaction(strData) 
                                        resStrList=resStr.split('<sep>',resStr.count('<sep>'))
                                        flag=resStrList[0]
                                        msg=resStrList[1]
                                    else:
                                        flag='True'
                                        msg='Success'
                                        
                                    if flag=='True':
                                        
                                        insertRes=db.sm_payment_collection.insert(cid=c_id,depot_id=depotId,depot_name=depot_name,sl=slNo,head_rowid=inv_rowid,store_id=store_id,store_name=store_name,order_sl=order_sl,order_datetime=order_datetime,delivery_date=delivery_date,payment_mode=payment_mode,credit_note=credit_note,client_id=client_id,client_name=client_name,rep_id=rep_id,
                                                                        rep_name=rep_name,market_id=market_id,market_name=market_name,d_man_id=d_man_id,d_man_name=d_man_name,area_id=area_id,area_name=area_name,level0_id=level0_id,level0_name=level0_name,level1_id=level1_id,level1_name=level1_name,level2_id=level2_id,level2_name=level2_name,level3_id=level3_id,level3_name=level3_name,cl_category_id=cl_category_id,cl_category_name=cl_category_name,cl_sub_category_id=cl_sub_category_id,cl_sub_category_name=cl_sub_category_name,special_territory_code=special_territory_code,invoice_date=invoice_date,
                                                                        invoice_ym_date=invoice_ym_date,collection_date=applied_date,ym_date=ym_date,payment_collection_date=applied_date,payment_ym_date=ym_date,collection_batch=collection_batch,collection_note=collection_note,shipment_no=shipment_no,doc_number=doc_number,receipt_description=receipt_description,transaction_type='Negative',transaction_cause=transaction_cause,collection_flag=collection_flag,total_inv_amount=total_amount,receivable_amount=receivable_amount,collection_amount=reverse_amount,status='Posted',rpt_trans_flag=1)
                                                                        
                                        mrNo = db.sm_payment_collection(insertRes).id
                                        
                                        #----------------------- Report Transaction ***
                                        try:
                                            collectonTp=round(actual_total_tp/total_amount*applied_amount,2)
                                            collectonVat=round(vat_total_amount/total_amount*applied_amount,2)
                                            collectonDisc=round(discount/total_amount*applied_amount,2)
                                            collectonSpDisc=round(sp_discount/total_amount*applied_amount,2)
                                        except:
                                            collectonTp=0
                                            collectonVat=0
                                            collectonDisc=0
                                            collectonSpDisc=0
                                            
                                        transaction_date=current_date
                                        db.sm_rpt_transaction.insert(cid=c_id,depot_id=depotId,depot_name=depot_name,store_id=store_id,store_name=store_name,inv_rowid=inv_rowid,inv_sl=slNo,invoice_date=invoice_date,transaction_type='PAYADJN',transaction_date=transaction_date,transaction_ref=mrNo,transaction_ref_date=applied_date,trans_net_amt=applied_amount,tp_amt=collectonTp,vat_amt=collectonVat,disc_amt=collectonDisc,spdisc_amt=collectonSpDisc,adjust_amount=transaction_adjust_amount,
                                                                 delivery_date=delivery_date,payment_mode=payment_mode,credit_note=credit_note,client_id=client_id,client_name=client_name,cl_category_id=cl_category_id,cl_category_name=cl_category_name,cl_sub_category_id=cl_sub_category_id,cl_sub_category_name=cl_sub_category_name,client_limit_amt=client_limit_amt,
                                                                 rep_id=rep_id,rep_name=rep_name,market_id=market_id,market_name=market_name,d_man_id=d_man_id,d_man_name=d_man_name,level0_id=level0_id,level0_name=level0_name,level1_id=level1_id,level1_name=level1_name,level2_id=level2_id,level2_name=level2_name,area_id=area_id,area_name=area_name,shipment_no=shipment_no,note=collection_note)
                                        #------------------
                                        
                                        #Update status of head and detail
                                        
                                        db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==depotId) & (db.sm_invoice_head.id==inv_rowid)).update(collection_amount=totalCollectAmount,adjust_amount=totalAdjustAmount)
                                        
                                        response.flash='Successfully submitted Decrease(Reversed) Adjustment TK. '+str(applied_amount)+'/= Customer: '+str(client_id)+'-'+str(client_name)
                                    else:
                                        response.flash='Process failed'
                                        
                            elif transaction_type=='Positive':                                
                                totalCollectAmount=round(collection_amount+applied_amount,2)
                                dueAmount=round((total_amount-returnAmount)-collection_amount,2)
                                
                                totalAdjustAmount=adjust_amount
                                transaction_adjust_amount=0
                                if collection_flag==0:
                                    totalAdjustAmount=round(adjust_amount+applied_amount,2)
                                    transaction_adjust_amount=applied_amount
                                    
                                if totalCollectAmount > (total_amount-returnAmount):
                                    response.flash='Increase amount can be maximum Tk.'+str(dueAmount)
                                    
                                else:
                                    #--------------------------------
                                    resStr=''
                                    
                                    if session.ledgerCreate=='YES':
                                        strData=str(c_id)+'<fdfd>CLTPAYMENT<fdfd>'+str(slNo)+'<fdfd>'+str(datetime_fixed)+'<fdfd>'+str(depotId)+'-'+str(slNo)+'<fdfd>CLT-'+str(client_id)+'<fdfd>DPT-'+str(depotId)+'<fdfd>'+str(applied_amount)
                                        resStr=set_balance_transaction(strData) 
                                        resStrList=resStr.split('<sep>',resStr.count('<sep>'))
                                        flag=resStrList[0]
                                        msg=resStrList[1]
                                    else:
                                        flag='True'
                                        msg='Success'
                                        
                                    if flag=='True':
                                        
                                        insertRes=db.sm_payment_collection.insert(cid=c_id,depot_id=depotId,depot_name=depot_name,sl=slNo,head_rowid=inv_rowid,store_id=store_id,store_name=store_name,order_sl=order_sl,order_datetime=order_datetime,delivery_date=delivery_date,payment_mode=payment_mode,credit_note=credit_note,client_id=client_id,client_name=client_name,rep_id=rep_id,
                                                                        rep_name=rep_name,market_id=market_id,market_name=market_name,d_man_id=d_man_id,d_man_name=d_man_name,area_id=area_id,area_name=area_name,level0_id=level0_id,level0_name=level0_name,level1_id=level1_id,level1_name=level1_name,level2_id=level2_id,level2_name=level2_name,level3_id=level3_id,level3_name=level3_name,cl_category_id=cl_category_id,cl_category_name=cl_category_name,cl_sub_category_id=cl_sub_category_id,cl_sub_category_name=cl_sub_category_name,special_territory_code=special_territory_code,invoice_date=invoice_date,
                                                                        invoice_ym_date=invoice_ym_date,collection_date=applied_date,ym_date=ym_date,payment_collection_date=applied_date,payment_ym_date=ym_date,collection_batch=collection_batch,collection_note=collection_note,shipment_no=shipment_no,doc_number=doc_number,receipt_description=receipt_description,transaction_type='Positive',transaction_cause=transaction_cause,collection_flag=collection_flag,total_inv_amount=total_amount,receivable_amount=receivable_amount,collection_amount=applied_amount,status='Posted',rpt_trans_flag=1)
                                        
                                        mrNo = db.sm_payment_collection(insertRes).id
                                        
                                        #----------------------- Report Transaction ***
                                        try:
                                            collectonTp=round(actual_total_tp/total_amount*applied_amount,2)
                                            collectonVat=round(vat_total_amount/total_amount*applied_amount,2)
                                            collectonDisc=round(discount/total_amount*applied_amount,2)
                                            collectonSpDisc=round(sp_discount/total_amount*applied_amount,2)
                                        except:
                                            collectonTp=0
                                            collectonVat=0
                                            collectonDisc=0
                                            collectonSpDisc=0
                                            
                                        transaction_date=current_date
                                        db.sm_rpt_transaction.insert(cid=c_id,depot_id=depotId,depot_name=depot_name,store_id=store_id,store_name=store_name,inv_rowid=inv_rowid,inv_sl=slNo,invoice_date=invoice_date,transaction_type='PAYADJP',transaction_date=transaction_date,transaction_ref=mrNo,transaction_ref_date=applied_date,trans_net_amt=applied_amount*(-1),tp_amt=collectonTp*(-1),vat_amt=collectonVat*(-1),disc_amt=collectonDisc*(-1),spdisc_amt=collectonSpDisc*(-1),adjust_amount=transaction_adjust_amount*(-1),
                                                                 delivery_date=delivery_date,payment_mode=payment_mode,credit_note=credit_note,client_id=client_id,client_name=client_name,cl_category_id=cl_category_id,cl_category_name=cl_category_name,cl_sub_category_id=cl_sub_category_id,cl_sub_category_name=cl_sub_category_name,client_limit_amt=client_limit_amt,
                                                                 rep_id=rep_id,rep_name=rep_name,market_id=market_id,market_name=market_name,d_man_id=d_man_id,d_man_name=d_man_name,level0_id=level0_id,level0_name=level0_name,level1_id=level1_id,level1_name=level1_name,level2_id=level2_id,level2_name=level2_name,area_id=area_id,area_name=area_name,shipment_no=shipment_no,note=collection_note)
                                        #------------------
                                        
                                        #Update status of head and detail
                                        db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==depotId) & (db.sm_invoice_head.id==inv_rowid)).update(collection_amount=totalCollectAmount,adjust_amount=totalAdjustAmount)
                                        
                                        response.flash='Successfully submitted Increase Adjustment TK. '+str(applied_amount)+'/= Customer: '+str(client_id)+'-'+str(client_name)
                                    else:
                                        response.flash='Process failed'
            
    return dict(causeRows=causeRows)



#========================= Payment collect single
def update_collection_bak():
    c_id=session.cid
    
    depotId=request.vars.depotId
    rowId=request.vars.rowId
    vslList=request.vars.vslList
    
    try:
        appliedAmount=float(request.vars.appliedAmount)
    except:
        appliedAmount=0
        
    if vslList==None:
        session.flash='Required checked confirmation'
        redirect (URL('collection_list'))
        
    elif appliedAmount<=0:
        session.flash='Required valid applied amount'
        redirect (URL('collection_list'))
    else:
        existRow=db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==depotId) & (db.sm_invoice_head.id==rowId)).select(db.sm_invoice_head.ALL,limitby=(0,1))
        if not existRow:
            session.flash='Required valid request'
            redirect (URL('collection_list'))
        else:
            slNo=existRow[0].sl
            depot_name=existRow[0].depot_name
            store_id=existRow[0].store_id
            store_name=existRow[0].store_name
            order_sl=existRow[0].order_sl
            order_datetime=existRow[0].order_datetime
            delivery_date=existRow[0].delivery_date
            payment_mode=existRow[0].payment_mode
            rep_id=existRow[0].rep_id
            rep_name=existRow[0].rep_name
            d_man_id=existRow[0].d_man_id
            d_man_name=existRow[0].d_man_name
            area_id=existRow[0].area_id
            area_name=existRow[0].area_name
            level0_id=existRow[0].level0_id
            level0_name=existRow[0].level0_name
            level1_id=existRow[0].level1_id
            level1_name=existRow[0].level1_name
            level2_id=existRow[0].level2_id
            level2_name=existRow[0].level2_name
            level3_id=existRow[0].level3_id
            level3_name=existRow[0].level3_name
            invoice_date=existRow[0].invoice_date
            invoice_ym_date=existRow[0].invoice_ym_date
            
            collection_batch=''
            collection_note=''
            shipment_no=''
            doc_number=''
            receipt_description=''            
            collection_date=current_date
            ym_date=str(collection_date)[0:7] + '-01'
            
            client_id=existRow[0].client_id
            client_name=existRow[0].client_name
            total_amount=float(existRow[0].total_amount)
            collection_amount=float(existRow[0].collection_amount)
            
            return_tp=float(existRow[0].return_tp)
            return_vat=float(existRow[0].return_vat)
            return_discount=float(existRow[0].return_discount)
            
            returnAmount=round(float(return_tp+return_vat-return_discount),2)
            
            receivable_amount=round(total_amount-returnAmount-collection_amount,2)
            appliedAmount=round(appliedAmount,2)            
            totalCollectAmount=round(collection_amount+appliedAmount,2)
            
            if totalCollectAmount > (total_amount-returnAmount):
                session.flash='Applied amount can not be greater than due amount'
                redirect (URL('collection_list'))
            else:
                #--------------------------------
                resStr=''                
                
                if session.ledgerCreate=='YES':
                    strData=str(c_id)+'<fdfd>CLTPAYMENT<fdfd>'+str(slNo)+'<fdfd>'+str(datetime_fixed)+'<fdfd>'+str(depotId)+'-'+str(slNo)+'<fdfd>CLT-'+str(client_id)+'<fdfd>DPT-'+str(depotId)+'<fdfd>'+str(appliedAmount)
                    resStr=set_balance_transaction(strData) 
                    resStrList=resStr.split('<sep>',resStr.count('<sep>'))
                    flag=resStrList[0]
                    msg=resStrList[1]
                else:
                    flag='True'
                    msg='Success'
                    
                if flag=='True':
                    #Update status of head and detail
                    #session.flash=msg
                    db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==depotId) & (db.sm_invoice_head.id==rowId)).update(collection_amount=totalCollectAmount)
                    
                    db.sm_payment_collection.insert(cid=c_id,depot_id=depotId,depot_name=depot_name,sl=slNo,head_rowid=rowId,store_id=store_id,store_name=store_name,order_sl=order_sl,order_datetime=order_datetime,delivery_date=delivery_date,payment_mode=payment_mode,client_id=client_id,client_name=client_name,rep_id=rep_id,
                                                    rep_name=rep_name,d_man_id=d_man_id,d_man_name=d_man_name,area_id=area_id,area_name=area_name,level0_id=level0_id,level0_name=level0_name,level1_id=level1_id,level1_name=level1_name,level2_id=level2_id,level2_name=level2_name,level3_id=level3_id,level3_name=level3_name,invoice_date=invoice_date,
                                                    invoice_ym_date=invoice_ym_date,collection_date=collection_date,ym_date=ym_date,collection_batch=collection_batch,collection_note=collection_note,shipment_no=shipment_no,doc_number=doc_number,receipt_description=receipt_description,transaction_type='Payment',total_inv_amount=total_amount,receivable_amount=receivable_amount,collection_amount=appliedAmount,status='Posted')
                    
                    session.flash='Successfully collected TK. '+str(appliedAmount)+'/= From '+str(client_id)+'-'+str(client_name)
                else:
                    session.flash='Process failed'
                
                redirect (URL('collection_list'))


#=======================payment List
def payment_list():
    c_id=session.cid
    
    #Check access permission
    #----------Task assaign----------
    task_id='rm_client_payment_manage'
    access_permission=check_role(task_id)
    if (access_permission==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    
    response.title='Payment List'
    
    #Set text for filter    
    btn_filter_payment=request.vars.btn_filter
    btn_all=request.vars.btn_all
    
    search_from_dt_pl=str(request.vars.from_dt).strip()
    search_to_dt_pl=str(request.vars.to_dt).strip()
    dp_id=str(request.vars.dp_id).strip()
    territory_id=str(request.vars.territory_id).strip()
    payment_type=str(request.vars.payment_type).strip()
    collection_batch=str(request.vars.collection_batch).strip()
    transaction_type=str(request.vars.transaction_type).strip()
    
    payment_customer_id=str(request.vars.payment_customer_id).strip()    
    payment_inv_sl=str(request.vars.payment_inv_sl).strip()
    payment_userid=str(request.vars.payment_userid).strip()
    
    reqPage=len(request.args)
    # Set sessions for filter
    if btn_filter_payment:
        session.btn_filter_payment=btn_filter_payment        
        session.dp_id=dp_id
        session.territory_id=territory_id
        session.payment_type=payment_type
        session.collection_batch=collection_batch
        session.transaction_type=transaction_type
        
        session.payment_customer_id=payment_customer_id
        session.payment_userid=payment_userid
        
        try:
            if payment_inv_sl!='':
                payment_inv_sl=int(payment_inv_sl)
                session.payment_inv_sl=payment_inv_sl            
        except:
            session.payment_inv_sl=''
            
            
        #---
        try:
            search_from_dt_pl=datetime.datetime.strptime(search_from_dt_pl,'%Y-%m-%d').strftime('%Y-%m-%d')
            session.search_from_dt_pl=search_from_dt_pl
        except:
            session.search_from_dt_pl=''
            
        #---
        try:
            search_to_dt_pl=datetime.datetime.strptime(search_to_dt_pl,'%Y-%m-%d').strftime('%Y-%m-%d')
            session.search_to_dt_pl=search_to_dt_pl
        except:
            session.search_to_dt_pl=''
            
        reqPage=0
        
    elif btn_all:
        session.btn_filter_payment=None
        session.dp_id=None
        session.territory_id=None
        session.payment_type=None
        session.search_from_dt_pl=None
        session.search_to_dt_pl=''        
        session.collection_batch=None
        session.payment_customer_id=None
        session.payment_inv_sl=None
        session.payment_userid=None
        reqPage=0
        
    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=(session.items_per_page)*2
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging  
    
    # Set query based on search type
    
    
    totalRecords=0
    
    qset=db()
    qset=qset(db.sm_payment_collection.cid==c_id)
    
    if (session.user_type!='Depot'):
        records=''
        response.flash='Only depot user can show payment'
    else:
        qset=qset(db.sm_payment_collection.depot_id==session.depot_id)
        
        if (session.btn_filter_payment):
            if (session.search_from_dt_pl=='' or session.search_from_dt_pl==None) and (not (session.search_to_dt_pl=='' or session.search_to_dt_pl==None)):
                qset=qset(db.sm_payment_collection.collection_date==session.search_to_dt_pl)
            else:
                if not (session.search_from_dt_pl=='' or session.search_from_dt_pl==None):
                    qset=qset(db.sm_payment_collection.collection_date>=session.search_from_dt_pl)
                    
                if not (session.search_to_dt_pl=='' or session.search_to_dt_pl==None):
                    qset=qset(db.sm_payment_collection.collection_date<=session.search_to_dt_pl)
                    
            #------------
            if not (session.dp_id=='' or session.dp_id==None):
                dp_id=str(session.dp_id).split('|')[0]
                qset=qset(db.sm_payment_collection.d_man_id==dp_id)
                
            #------------
            if not (session.territory_id=='' or session.territory_id==None):
                territory_id=str(session.territory_id).split('|')[0]
                qset=qset(db.sm_payment_collection.area_id==territory_id)
                
            #------------
            if not (session.payment_customer_id=='' or session.payment_customer_id==None):
                payment_customer_id=str(session.payment_customer_id).split('|')[0]
                qset=qset(db.sm_payment_collection.client_id==payment_customer_id)
                
            #------------
            if not (session.payment_inv_sl=='' or session.payment_inv_sl==None):
                payment_inv_sl=session.payment_inv_sl
                qset=qset(db.sm_payment_collection.sl==payment_inv_sl)
                
            if not (session.payment_type=='' or session.payment_type==None):
                payment_type=str(session.payment_type)
                qset=qset(db.sm_payment_collection.payment_type==payment_type)
                
            if not (session.collection_batch=='' or session.collection_batch==None):
                collection_batch=str(session.collection_batch)
                qset=qset(db.sm_payment_collection.collection_batch==collection_batch)
                
            if not (session.transaction_type=='' or session.transaction_type==None):
                transaction_type=str(session.transaction_type)
                qset=qset(db.sm_payment_collection.transaction_type==transaction_type)
            
            if not (session.payment_userid=='' or session.payment_userid==None):
                payment_userid=str(session.payment_userid).split('|')[0]
                qset=qset(db.sm_payment_collection.created_by==payment_userid)
            
    records=qset.select(db.sm_payment_collection.ALL,orderby=~db.sm_payment_collection.id,limitby=limitby)
    totalRecords=qset.count()
    
    #------------ filter form
    filterform =SQLFORM(db.sm_search_date,
                  fields=['from_dt','to_dt']
                  )
    
    if (session.search_from_dt_pl=='' or session.search_from_dt_pl==None):
        filterform.vars.from_dt=''
    else:
        filterform.vars.from_dt=session.search_from_dt_pl
        
    if (session.search_to_dt_pl==None):
        filterform.vars.to_dt=current_date
    else:
        filterform.vars.to_dt=session.search_to_dt_pl
        
    if filterform.accepts(request.vars,session):
        pass
        
    paymentTypeRows=db((db.sm_category_type.cid==session.cid) & (db.sm_category_type.type_name=='PAYMENT_TYPE')).select(db.sm_category_type.cat_type_id,orderby=db.sm_category_type.cat_type_id)
    
    return dict(records=records,filterform=filterform,totalRecords=totalRecords,paymentTypeRows=paymentTypeRows,page=page,items_per_page=items_per_page,access_permission=access_permission)


def preview_payment():
    #----------Task assaign----------
    task_id='rm_client_payment_manage'
    access_permission=check_role(task_id)
    if (access_permission==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
        
    #------------------------
    c_id=session.cid
    depot_id=request.vars.depotId
    refid=request.vars.refid
    
    #--------------- Title
    response.title='Preview Client Payment'
    
    
    sl=0
    client_id=''
    client_address=''
    
    records=db((db.sm_payment_collection.cid==c_id) & (db.sm_payment_collection.depot_id==depot_id)& (db.sm_payment_collection.id==refid)).select(db.sm_payment_collection.ALL,limitby=(0,1))
    if not records:
        session.flash='Invalid Request'
        redirect (URL('payment_list'))
    else:
        client_id=records[0].client_id
        
        check_client=db((db.sm_client.cid==c_id) & (db.sm_client.client_id==client_id)).select(db.sm_client.address,limitby=(0,1))
        if check_client:
            client_address=check_client[0].address
            
    #-----------  
    return dict(records=records,client_address=client_address)

#===================================== Download
def download_payment_list():
    #----------Task assaign----------
    task_id='rm_client_payment_manage'
    task_id_view='rm_client_payment_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('payment_list'))      
        
    #   ---------------------
    c_id=session.cid
    records=''
    
    qset=db()
    qset=qset(db.sm_payment_collection.cid==c_id)
    
    if (session.user_type!='Depot'):
        records=''
        response.flash='Only depot user can show payment'
    else:
        qset=qset(db.sm_payment_collection.depot_id==session.depot_id)
        
        if (session.btn_filter_payment):            
            if (session.search_from_dt_pl=='' or session.search_from_dt_pl==None) and (not (session.search_to_dt_pl=='' or session.search_to_dt_pl==None)):
                qset=qset(db.sm_payment_collection.collection_date==session.search_to_dt_pl)
            else:
                if not (session.search_from_dt_pl=='' or session.search_from_dt_pl==None):
                    qset=qset(db.sm_payment_collection.collection_date>=session.search_from_dt_pl)
                    
                if not (session.search_to_dt_pl=='' or session.search_to_dt_pl==None):
                    qset=qset(db.sm_payment_collection.collection_date<=session.search_to_dt_pl)
                    
            #------------
            if not (session.dp_id=='' or session.dp_id==None):
                dp_id=str(session.dp_id).split('|')[0]
                qset=qset(db.sm_payment_collection.d_man_id==dp_id)
                
            #------------
            if not (session.territory_id=='' or session.territory_id==None):
                territory_id=str(session.territory_id).split('|')[0]
                qset=qset(db.sm_payment_collection.area_id==territory_id)
                
            #------------
            if not (session.payment_customer_id=='' or session.payment_customer_id==None):
                payment_customer_id=str(session.payment_customer_id).split('|')[0]
                qset=qset(db.sm_payment_collection.client_id==payment_customer_id)
                
            #------------
            if not (session.payment_inv_sl=='' or session.payment_inv_sl==None):
                payment_inv_sl=session.payment_inv_sl
                qset=qset(db.sm_payment_collection.sl==payment_inv_sl)
                
            if not (session.payment_type=='' or session.payment_type==None):
                payment_type=str(session.payment_type)
                qset=qset(db.sm_payment_collection.payment_type==payment_type)
            
            if not (session.collection_batch=='' or session.collection_batch==None):
                collection_batch=str(session.collection_batch)
                qset=qset(db.sm_payment_collection.collection_batch==collection_batch)
            
            if not (session.transaction_type=='' or session.transaction_type==None):
                transaction_type=str(session.transaction_type)
                qset=qset(db.sm_payment_collection.transaction_type==transaction_type)
            
            if not (session.payment_userid=='' or session.payment_userid==None):
                payment_userid=str(session.payment_userid).split('|')[0]
                qset=qset(db.sm_payment_collection.created_by==payment_userid)
                
    records=qset.select(db.sm_payment_collection.ALL,orderby=~db.sm_payment_collection.id)
    
    #---------
    myString='Payment List \n\n'
    myString+='INV.SL,Ref.,Territory,Customer ID,Customer Name,DP ID,DP Name,Collection Date,Collected By,Transaction Type,Inv. Amount,Transaction  Amount,Payment Type,Notes,Batch\n'
    for rec in records:
        depot_id=str(rec.depot_id)
        depot_name=str(rec.depot_name).replace(',', ' ')
        
        sl=str(rec.sl)
        head_rowid=str(rec.head_rowid)
        client_id=str(rec.client_id)
        client_name=str(rec.client_name).replace(',', ' ')
        rep_id=str(rec.rep_id)
        rep_name=str(rec.rep_name).replace(',', ' ')
        
        payment_mode=str(rec.payment_mode)
        payment_type=str(rec.payment_type)  
        
        delivery_date=str(rec.delivery_date)
        invoice_date=str(rec.invoice_date)
        
        d_man_id=str(rec.d_man_id)
        d_man_name=str(rec.d_man_name).replace(',', ' ')
        
        area_id=str(rec.area_id)
        area_name=str(rec.area_name).replace(',', ' ')
        collection_date=str(rec.collection_date)
        collection_note=str(rec.collection_note).replace(',', ' ')
        collection_batch=str(rec.collection_batch)
        receipt_description=str(rec.receipt_description).replace(',', ' ')   
        
        transaction_type=str(rec.transaction_type)
        total_inv_amount=str(rec.total_inv_amount)
        collection_amount=str(rec.collection_amount)
        created_by=str(rec.created_by)
        
        myString+='INV'+depot_id+'-'+sl+','+head_rowid+','+area_id+','+client_id+','+client_name+','+d_man_id+','+d_man_name+','+collection_date+','+created_by+','+transaction_type+','+total_inv_amount+','+collection_amount+','+payment_type+','+collection_note+','+collection_batch+'\n'
    
    #-----------
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_payment.csv'
    return str(myString)
    
