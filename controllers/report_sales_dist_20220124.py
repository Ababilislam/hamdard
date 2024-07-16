import calendar


def get_dist_list():
    retStr = ''
    cid = session.cid

    if session.user_type == 'Depot':
        rows = db((db.sm_depot_distributor.cid == cid) & (db.sm_depot_distributor.depot_id == session.depot_id)).select(
            db.sm_depot_distributor.dist_id, db.sm_depot_distributor.dist_name,groupby=db.sm_depot_distributor.dist_id, orderby=db.sm_depot_distributor.dist_name)
    else:
        rows = db(db.sm_depot_distributor.cid == cid).select(db.sm_depot_distributor.dist_id, db.sm_depot_distributor.dist_name,groupby=db.sm_depot_distributor.dist_id, orderby=db.sm_depot_distributor.dist_name)

    for row in rows:
        dist_id = str(row.dist_id)
        dist_name = str(row.dist_name).replace('|', ' ').replace(',', ' ')

        if retStr == '':
            retStr = dist_id + '|' + dist_name
        else:
            retStr += ',' + dist_id + '|' + dist_name

    return retStr

def get_dist_depot_list():
    retStr = ''
    cid = session.cid
    dist_id=request.vars.dist_id


    if session.user_type == 'Depot':
        rows = db((db.sm_depot_distributor.cid == cid) & (db.sm_depot_distributor.dist_id == dist_id) & (db.sm_depot_distributor.depot_id == session.depot_id)).select(
            db.sm_depot_distributor.depot_id, db.sm_depot_distributor.depot_name,orderby=db.sm_depot_distributor.depot_name)
    else:
        rows = db((db.sm_depot_distributor.cid == cid) & (db.sm_depot_distributor.dist_id == dist_id)).select(db.sm_depot_distributor.depot_id, db.sm_depot_distributor.depot_name, orderby=db.sm_depot_distributor.depot_id)

    for row in rows:
        depot_id = str(row.depot_id)
        depot_name = str(row.depot_name).replace('|', ' ').replace(',', ' ')

        if retStr == '':
            retStr = depot_id + '|' + depot_name
        else:
            retStr += ',' + depot_id + '|' + depot_name

    return retStr


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
        
    response.title='Report:Sales Distributor'
    
    c_id=session.cid
    
    search_form =SQLFORM(db.sm_search_date)
    
    search_form.vars.from_dt_3=''
    search_form.vars.to_dt_3=''
    if search_form.accepts(request.vars,session):    
        pass
    
    #-------------Billal
    btn_inv_preview=request.vars.btn_inv_preview
    btn_return_note_preview=request.vars.btn_return_note_preview
    btn_invoice_item_sd_afterDel = request.vars.btn_invoice_item_sd_afterDel

    if btn_inv_preview or btn_return_note_preview or btn_invoice_item_sd_afterDel:
        date_from=request.vars.to_dt_2 #request.vars.from_dt_2
        date_to=request.vars.to_dt_2

        dist = str(request.vars.dist)
        depot = str(request.vars.depot_id)


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
            if dateDiff>1:
                response.flash="1 days allowed between Date Range"
            else:
                dateFlagRet=True
                

                    
                if dateFlagRet==False:
                    response.flash="Invalid Return Date Range"
                else:
                    if dist=='':
                        session.flash="Required Distributor"
                        redirect(URL(c='report_sales_dist',f='home'))
                    else:
                        if depot == '':
                            session.flash = "Required Depot"
                            redirect(URL(c='report_sales_dist', f='home'))
                        else:
                            if dist!='':
                                dist_id=dist.split('|')[0].upper().strip()
                            else:
                                dist_id=dist

                            if depot!='':
                                depot_id=depot.split('|')[0].upper().strip()
                            else:
                                depot_id=depot

                            if btn_inv_preview:
                                redirect (URL('inv_preview_dist',vars=dict(date_from=date_from,date_to=date_to,dist_id=dist_id,depot_id=depot_id)))
                            elif btn_return_note_preview:
                                redirect (URL('return_note_preview_dist',vars=dict(date_from=date_from,date_to=date_to,dist_id=dist_id,depot_id=depot_id)))
                            elif btn_invoice_item_sd_afterDel:
                                redirect (URL('invoice_item_list_synopsis_sd_after_del_dist',vars=dict(date_from=date_from,date_to=date_to,dist_id=dist_id,depot_id=depot_id)))

    depotDistRows=''
    if session.user_type == 'Depot':
        depotDistRows = db((db.sm_depot_distributor.cid == c_id) & (db.sm_depot_distributor.depot_id == session.depot_id)).select(
            db.sm_depot_distributor.depot_id, db.sm_depot_distributor.depot_name,db.sm_depot_distributor.dist_id, db.sm_depot_distributor.dist_name,limitby=(0,1))



    return dict(search_form=search_form,depotDistRows=depotDistRows)


def inv_preview_dist():
    c_id = session.cid

    # --------------- Title
    response.title = 'Preview Invoice Distributor'

    fromDate = request.vars.date_from
    toDate = request.vars.date_to

    dist_id = str(request.vars.dist_id).strip()
    depot_id = str(request.vars.depot_id).strip()


    dist_name = ''
    dist_disc_percent=0
    distRow = db((db.sm_depot_distributor.cid == c_id) & (db.sm_depot_distributor.dist_id == dist_id)).select(
        db.sm_depot_distributor.depot_id, db.sm_depot_distributor.dist_name,db.sm_depot_distributor.dist_disc_percent, limitby=(0, 1))

    if distRow:
        dist_name = distRow[0].dist_name
        dist_disc_percent = distRow[0].dist_disc_percent

        depot_id_list = []
        if depot_id=='':
            distRow1 = db((db.sm_depot_distributor.cid == c_id) & (db.sm_depot_distributor.dist_id == dist_id)).select(
                db.sm_depot_distributor.depot_id, db.sm_depot_distributor.dist_name,
                db.sm_depot_distributor.dist_disc_percent)

            for row in distRow1:
                depot_id = row.depot_id
                depot_id_list.append(depot_id)

        try:
            startDt = datetime.datetime.strptime(str(fromDate), '%Y-%m-%d').strftime('%Y-%m-%d')
        except:
            startDt = ''

        endDt = datetime.datetime.strptime(str(toDate), '%Y-%m-%d').strftime('%Y-%m-%d')

        data_List=[]
        # -----------
        #depot_id = ''
        depot_name = ''
        store_id = ''
        store_name = ''
        sl = 0
        order_sl = 0
        order_datetime = ''
        delivery_date = ''
        client_id = ''
        client_name = ''
        rep_id = ''
        rep_name = ''
        area_id = ''
        area_name = ''
        payment_mode = ''
        discount = 0
        note = ''
        status = ''
        level0_id = ''
        level0_name = ''
        discount_precent = 0
        collection_amount = 0
        collection_amount = 0
        regular_disc_tp = 0

        qset=db()
        qset=qset(db.sm_invoice_head.cid == c_id)

        if depot_id == '':
            qset = qset(db.sm_invoice_head.depot_id.belongs(depot_id_list))
        else:
            qset = qset(db.sm_invoice_head.depot_id == depot_id)

        qset = qset(db.sm_invoice_head.invoice_date == endDt)
        qset = qset(db.sm_invoice_head.status == 'Invoiced')
        hRecords = qset.select(db.sm_invoice_head.ALL,db.sm_invoice_head.dist_discount.sum(),groupby=db.sm_invoice_head.invoice_date, limitby=(0, 1))

        if hRecords:
            depot_id = hRecords[0][db.sm_invoice_head.depot_id]
            depot_name = hRecords[0][db.sm_invoice_head.depot_name]
            sl ='' # hRecords[0].sl
            store_id ='' # hRecords[0].store_id
            store_name ='' # hRecords[0].store_name
            order_sl ='' # hRecords[0].order_sl
            order_datetime ='' # hRecords[0].order_datetime
            delivery_date ='' # hRecords[0].delivery_date
            invoice_date = hRecords[0][db.sm_invoice_head.invoice_date]
            client_id ='' # hRecords[0].client_id
            client_name ='' # hRecords[0].client_name
            rep_id ='' # hRecords[0].rep_id
            rep_name ='' # hRecords[0].rep_name
            d_man_id ='' # hRecords[0].d_man_id
            d_man_name ='' # hRecords[0].d_man_name
            area_id ='' # hRecords[0].area_id
            area_name ='' # hRecords[0].area_name
            payment_mode ='' # hRecords[0].payment_mode
            credit_note ='' # hRecords[0].credit_note
            discount =0 # hRecords[0].discount
            note ='' # hRecords[0].note
            status ='' # hRecords[0].status
            updated_by ='' # hRecords[0].updated_by
            level0_id ='' # hRecords[0].level0_id
            level0_name ='' # hRecords[0].level0_name
            level1_id ='' # hRecords[0].level1_id
            level1_name ='' # hRecords[0].level1_name
            level2_id ='' # hRecords[0].level2_id
            level2_name ='' # hRecords[0].level2_name
            discount_precent =0 # hRecords[0].discount_precent
            collection_amount =0 # hRecords[0].collection_amount
            regular_disc_tp =0 # hRecords[0].regular_disc_tp
            posted_by ='' # hRecords[0].posted_by
            return_tp =0 # hRecords[0].return_tp
            return_vat =0 # hRecords[0].return_vat
            return_discount =0 # hRecords[0].return_discount
            return_sp_discount =0 # hRecords[0].return_sp_discount

            discount_precent=dist_disc_percent

            dist_discount=hRecords[0][db.sm_invoice_head.dist_discount.sum()]
            discount=dist_discount

            address = ''
            client_category = ''
            owner_name = ''
            contact_no1 = ''
            district = ''
            client_old_id = ''
            sub_category_name = ''
            market_id = ''
            market_name = ''

            # clientRow = db((db.sm_client.cid == c_id) & (db.sm_client.client_id == client_id)).select(db.sm_client.ALL,
            #                                                                                           limitby=(0, 1))
            # if clientRow:
            #     address = clientRow[0].address
            #     client_category = clientRow[0].category_id
            #     owner_name = clientRow[0].owner_name
            #     contact_no1 = clientRow[0].contact_no1
            #     district = clientRow[0].district
            #     client_old_id = clientRow[0].client_old_id
            #     sub_category_name = clientRow[0].sub_category_name
            #     market_id = clientRow[0].market_id
            #     market_name = clientRow[0].market_name
            # --------------------
            p_sl = 0
            vdDictList = []

            records = db((db.sm_invoice.cid == c_id) & (db.sm_invoice.depot_id == depot_id)& (db.sm_invoice.invoice_date == endDt)).select(db.sm_invoice.ALL,db.sm_invoice.quantity.sum(),db.sm_invoice.bonus_qty.sum(),groupby=db.sm_invoice.invoice_date|db.sm_invoice.item_id|db.sm_invoice.batch_id, orderby=db.sm_invoice.item_name)


            for vdRow in records:
                item_id = vdRow[db.sm_invoice.item_id]
                item_name = vdRow[db.sm_invoice.item_name]
                batch_id = vdRow[db.sm_invoice.batch_id]
                category_id = vdRow[db.sm_invoice.category_id]
                actual_tp = vdRow[db.sm_invoice.actual_tp]
                actual_vat = vdRow[db.sm_invoice.actual_vat]
                quantity = vdRow[db.sm_invoice.quantity.sum()]
                bonus_qty = vdRow[db.sm_invoice.bonus_qty.sum()]
                price = vdRow[db.sm_invoice.price]
                item_vat = vdRow[db.sm_invoice.item_vat]
                short_note = vdRow[db.sm_invoice.short_note]
                item_unit = vdRow[db.sm_invoice.item_unit]

                promotion_type = vdRow[db.sm_invoice.promotion_type]
                bonus_applied_on_qty = vdRow[db.sm_invoice.bonus_applied_on_qty]
                discount_type = vdRow[db.sm_invoice.discount_type]
                item_discount = vdRow[db.sm_invoice.item_discount]
                item_discount_percent = 0 #vdRow[db.sm_invoice.item_discount_percent]
                discount_type_quantity = vdRow[db.sm_invoice.discount_type_quantity]

                p_sl += 1
                # ------------------------
                vdDict = {'p_sl': p_sl, 'item_id': item_id, 'item_name': item_name, 'batch_id': batch_id,
                          'item_unit': item_unit, 'category_id': category_id, 'actual_tp': actual_tp,
                          'actual_vat': actual_vat, 'quantity': quantity, 'bonus_qty': bonus_qty, 'price': price,
                          'item_vat': item_vat, 'short_note': short_note, 'promotion_type': promotion_type,
                          'bonus_applied_on_qty': bonus_applied_on_qty, 'discount_type': discount_type,
                          'item_discount': item_discount, 'item_discount_percent': item_discount_percent,
                          'discount_type_quantity': discount_type_quantity}
                vdDictList.append(vdDict)

            vhDict = {'depot_id': depot_id, 'depot_name': depot_name, 'sl': sl, 'store_id': store_id,
                      'store_name': store_name, 'order_sl': order_sl, 'order_datetime': order_datetime,
                      'delivery_date': delivery_date, 'invoice_date': invoice_date, 'client_id': client_id,
                      'client_old_id': client_old_id, 'client_name': client_name, 'client_category': client_category,
                      'sub_category_name': sub_category_name, 'market_id': market_id, 'market_name': market_name,
                      'contact_no1': contact_no1, 'owner_name': owner_name, 'address': address, 'district': district,
                      'level0': level0_id, 'level0_name': level0_name, 'level1': level1_id, 'level1_name': level1_name,
                      'level2': level2_id, 'level2_name': level2_name, 'rep_id': rep_id, 'rep_name': rep_name,
                      'd_man_id': d_man_id, 'd_man_name': d_man_name, 'area_id': area_id, 'area_name': area_name,
                      'collection_amount': collection_amount, 'status': status, 'updated_by': updated_by,
                      'regular_disc_tp': regular_disc_tp, 'discount': discount, 'discount_precent': discount_precent,
                      'note': note, 'payment_mode': payment_mode, 'credit_note': credit_note, 'return_tp': return_tp,
                      'return_vat': return_vat, 'return_discount': return_discount,
                      'return_sp_discount': return_sp_discount, 'vdList': vdDictList}
            data_List.append(vhDict)

        if len(data_List)==0:
            response.flash='Data not available'

        # -------------------------
    return dict(data_List=data_List, dist_id=dist_id, dist_name=dist_name)


def return_note_preview_dist():
    c_id=session.cid
    
    response.title='5.2 Return Note Preview Distributor'
    
    fromDate=request.vars.date_from
    toDate=request.vars.date_to
    
    dist_id=str(request.vars.dist_id).strip()
    depot_id = str(request.vars.depot_id).strip()
    
    dist_name=''
    depot_id=''
    distRow=db((db.sm_depot_distributor.cid==c_id)&(db.sm_depot_distributor.dist_id==dist_id)).select(db.sm_depot_distributor.depot_id,db.sm_depot_distributor.dist_name,limitby=(0,1))
    if distRow:
        dist_name=distRow[0].dist_name
        depot_id = distRow[0].depot_id

        depot_id_list = []
        if depot_id == '':
            distRow1 = db((db.sm_depot_distributor.cid == c_id) & (db.sm_depot_distributor.dist_id == dist_id)).select(
                db.sm_depot_distributor.depot_id, db.sm_depot_distributor.dist_name,
                db.sm_depot_distributor.dist_disc_percent)

            for row in distRow1:
                depot_id = row.depot_id
                depot_id_list.append(depot_id)

        try:
            startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')
        except:
            startDt=''

        endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')

        #=============================
        qset=db()
        qset=qset(db.sm_return_head.cid==c_id)

        if depot_id == '':
            qset=qset(db.sm_return_head.depot_id.belongs(depot_id_list))
        else:
            qset = qset(db.sm_return_head.depot_id == depot_id)


        qset=qset((db.sm_return_head.return_date>=startDt)& (db.sm_return_head.return_date<=endDt))
        qset=qset(db.sm_return_head.status=='Returned')

        records=qset.select(db.sm_return_head.ALL,db.sm_return_head.inv_dist_discount.sum(),db.sm_return_head.dist_discount.sum(),groupby=db.sm_return_head.return_date,orderby=db.sm_return_head.sl)

        data_List=[]

        for row in records:
            depot_id=row[db.sm_return_head.depot_id] #row.depot_id
            depotName=row[db.sm_return_head.depot_name] #row.depot_name
            store_id=''#row.store_id
            store_name=''#row.store_name

            sl=''#row.sl
            order_sl=''#row.order_sl
            invoice_sl=''#row.invoice_sl
            return_date=row[db.sm_return_head.return_date] #row.return_date

            client_id=''#row.client_id
            client_name=''#row.client_name
            rep_id=''#row.rep_id
            rep_name=''#row.rep_name
            level0_name=''#row.level0_name
            level2_name=''#row.level2_name
            area_name=''#row.area_name

            discount=0#row.discount
            req_note=''#row.note
            status=''#row.status
            cause=''#row.ret_reason
            updatedBy=''#row.updated_by
            inv_discount=0 #row.inv_discount
            prev_return_discount=0 #row.prev_return_discount

            d_man_id=''#row.d_man_id
            d_man_name=''#row.d_man_name
            invoice_date=''#row.invoice_date.strftime('%d-%b-%Y')
            cl_category_name=''#row.cl_category_name
            market_name=''#row.market_name

            payment_mode=''
            order_date=''
            address=''
            contact_no1=''
            district=''

            inv_dist_discount=row[db.sm_return_head.inv_dist_discount.sum()]
            dist_discount = row[db.sm_return_head.dist_discount.sum()]

            discount=dist_discount
            inv_discount=inv_dist_discount


            detDictList=[]
            detailRows=db((db.sm_return.cid==c_id) & (db.sm_return.return_date==return_date)& (db.sm_return.status=='Returned')).select(db.sm_return.item_id,db.sm_return.item_name,db.sm_return.batch_id,db.sm_return.item_unit,db.sm_return.quantity.sum(),db.sm_return.bonus_qty.sum(),db.sm_return.actual_tp,db.sm_return.item_vat.sum(),db.sm_return.inv_quantity.sum(),db.sm_return.inv_bonus_qty.sum(),db.sm_return.inv_bonus_qty.sum(),db.sm_return.prev_return_qty.sum(),db.sm_return.prev_return_bonus_qty.sum(),db.sm_return.inv_price,db.sm_return.inv_item_vat.sum(),groupby=db.sm_return.item_id|db.sm_return.batch_id,orderby=db.sm_return.item_name)

            for dRow in detailRows:
                item_id=dRow[db.sm_return.item_id]
                item_name=dRow[db.sm_return.item_name]
                batch_id=dRow[db.sm_return.batch_id]
                item_unit=dRow[db.sm_return.item_unit]
                quantity=dRow[db.sm_return.quantity.sum()]
                bonus_qty=dRow[db.sm_return.bonus_qty.sum()]
                price=dRow[db.sm_return.actual_tp]
                item_vat=dRow[db.sm_return.item_vat.sum()]
                inv_quantity=dRow[db.sm_return.inv_quantity.sum()]
                inv_bonus_qty=dRow[db.sm_return.inv_bonus_qty.sum()]
                prev_return_qty=dRow[db.sm_return.prev_return_qty.sum()]
                prev_return_bonus_qty=dRow[db.sm_return.prev_return_bonus_qty.sum()]
                inv_price=dRow[db.sm_return.actual_tp]
                inv_item_vat=dRow[db.sm_return.inv_item_vat.sum()]

                #------------------------
                vdDict= {'item_id': item_id,'item_name': item_name,'batch_id':batch_id,'item_unit':item_unit,'quantity':quantity,'bonus_qty':bonus_qty,'price':price,'item_vat':item_vat,'inv_quantity':inv_quantity,'inv_bonus_qty': inv_bonus_qty,'prev_return_qty': prev_return_qty,'prev_return_bonus_qty': prev_return_bonus_qty,'inv_price': inv_price,'inv_item_vat': inv_item_vat}
                detDictList.append(vdDict)

            vhDict={'depot_id':depot_id,'depot_name':depotName,'sl':sl,'order_sl':order_sl,'invoice_sl':invoice_sl,'return_date':return_date,'client_id':client_id,'client_name':client_name,'rep_id':rep_id,'rep_name':rep_name,'req_note':req_note,'status':status,'discount':discount,'cause':cause,'updatedBy':updatedBy,'d_man_id':d_man_id,'d_man_name':d_man_name,'payment_mode':payment_mode,'inv_discount':inv_discount,'prev_return_discount':prev_return_discount,'invoice_date':invoice_date,'level0_name':level0_name,'level2_name':level2_name,'order_date':order_date,'address':address,'category_name':cl_category_name,'market_name':market_name,'contact_no1':contact_no1,'district':district,'area_name':area_name,'store_id':store_id,'store_name':store_name,'vdList':detDictList}
            data_List.append(vhDict)

        if len(data_List)==0:
            response.flash='Data not available'
    
    return dict(data_List=data_List,fromDate=fromDate,toDate=toDate,distID=dist_id,distName=dist_name)

    #-------------


def invoice_item_list_synopsis_sd_after_del_dist():
    c_id = session.cid

    # --------------- Title
    response.title = '5.1 Preview Synopsis SD With Batch After Delivery'

    fromDate = request.vars.date_from
    toDate = request.vars.date_to

    dist_id = str(request.vars.dist_id).strip()
    depot_id = str(request.vars.depot_id).strip()

    dist_name = ''
    depot_name = ''
    dist_disc_percent = 0
    distRow = db((db.sm_depot_distributor.cid == c_id) & (db.sm_depot_distributor.dist_id == dist_id)& (db.sm_depot_distributor.depot_id == depot_id)).select(db.sm_depot_distributor.dist_name,db.sm_depot_distributor.depot_name, db.sm_depot_distributor.dist_disc_percent,
        limitby=(0, 1))

    if distRow:
        dist_name = distRow[0].dist_name
        depot_name = distRow[0].depot_name
        dist_disc_percent = distRow[0].dist_disc_percent

        depot_id_list = []

        if depot_id == '':
            distRow1 = db((db.sm_depot_distributor.cid == c_id) & (db.sm_depot_distributor.dist_id == dist_id)).select(
                db.sm_depot_distributor.depot_id, db.sm_depot_distributor.dist_name,
                db.sm_depot_distributor.dist_disc_percent)

            for row in distRow1:
                depot_id = row.depot_id
                depot_id_list.append(depot_id)

        try:
            startDt = datetime.datetime.strptime(str(fromDate), '%Y-%m-%d').strftime('%Y-%m-%d')
        except:
            startDt = ''

        endDt = datetime.datetime.strptime(str(toDate), '%Y-%m-%d').strftime('%Y-%m-%d')

    # -------------
    invoice_dateFrom = ''
    invoice_dateTo = ''

    territory_id = ''
    territory_name = ''

    d_man_id = ''
    d_man_name = ''
    paymentMode = ''
    search_from_sl = ''
    search_to_sl = ''
    creditType = ''
    # ----------------------

    req_depot=depot_id

    qset = db()
    qset = qset(db.sm_invoice_head.cid == c_id)
    qset = qset(db.sm_invoice_head.invoice_date == endDt)
    qset = qset(db.sm_invoice_head.sl != 0)

    if depot_id == '':
        qset = qset(db.sm_invoice_head.depot_id.belongs(depot_id_list))
    else:
        qset = qset(db.sm_invoice_head.depot_id == depot_id)


    qset = qset(db.sm_invoice_head.status == 'Invoiced')


    headRecords1 = qset.select(db.sm_invoice_head.client_id, db.sm_invoice_head.id.count(),
                               db.sm_invoice_head.actual_total_tp.sum(), db.sm_invoice_head.total_amount.sum(),
                               db.sm_invoice_head.vat_total_amount.sum(), db.sm_invoice_head.discount.sum(),
                               db.sm_invoice_head.sp_discount.sum(), db.sm_invoice_head.return_tp.sum(),
                               db.sm_invoice_head.return_vat.sum(), db.sm_invoice_head.return_discount.sum(),
                               db.sm_invoice_head.return_sp_discount.sum(),db.sm_invoice_head.dist_discount.sum(), groupby=db.sm_invoice_head.client_id)
    clientCount = len(headRecords1)
    # ---------------------- maximum market Name
    maxMarketID = ''
    maxmarketName = ''
    maxCount = 0
    headRecords2 = qset.select(db.sm_invoice_head.market_id, db.sm_invoice_head.market_name.max(),
                               db.sm_invoice_head.id.count(), groupby=db.sm_invoice_head.market_id)
    for headRec2 in headRecords2:
        market_id = headRec2.sm_invoice_head.market_id
        market_name = headRec2[db.sm_invoice_head.market_name.max()]
        market_count = headRec2[db.sm_invoice_head.id.count()]
        if market_count > maxCount:
            maxMarketID = market_id
            maxmarketName = market_name
            maxCount = market_count
        else:
            continue

    # ------------------
    invoiceTotal = 0
    totalAmount = 0
    vatTotal = 0
    totalDiscount = 0
    totalSpDiscount = 0
    return_tp = 0
    return_vat = 0
    return_discount = 0
    actual_total_tp = 0
    ret_actual_total_tp=0
    return_sp_discount = 0

    headRecords = qset.select(db.sm_invoice_head.depot_id, db.sm_invoice_head.id.count(),
                              db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.ret_actual_total_tp.sum(), db.sm_invoice_head.total_amount.sum(),
                              db.sm_invoice_head.vat_total_amount.sum(), db.sm_invoice_head.discount.sum(),
                              db.sm_invoice_head.sp_discount.sum(), db.sm_invoice_head.return_tp.sum(),
                              db.sm_invoice_head.return_vat.sum(), db.sm_invoice_head.return_discount.sum(),
                              db.sm_invoice_head.return_sp_discount.sum(),db.sm_invoice_head.dist_discount.sum(),db.sm_invoice_head.ret_dist_discount.sum(), groupby=db.sm_invoice_head.depot_id)
    for hRow in headRecords:
        invoiceTotal += hRow[db.sm_invoice_head.id.count()]
        # actual_total_tp+=hRow[db.sm_invoice_head.actual_total_tp.sum()]
        totalAmount += hRow[db.sm_invoice_head.total_amount.sum()]
        # vatTotal+=hRow[db.sm_invoice_head.vat_total_amount.sum()]
        #totalDiscount += hRow[db.sm_invoice_head.discount.sum()]
        # totalSpDiscount+=hRow[db.sm_invoice_head.sp_discount.sum()]
        ret_actual_total_tp += hRow[db.sm_invoice_head.ret_actual_total_tp.sum()]
        return_tp += hRow[db.sm_invoice_head.return_tp.sum()]
        return_vat += hRow[db.sm_invoice_head.return_vat.sum()]
        #return_discount += hRow[db.sm_invoice_head.return_discount.sum()]
        #return_sp_discount += hRow[db.sm_invoice_head.return_sp_discount.sum()]
        totalDiscount += hRow[db.sm_invoice_head.dist_discount.sum()]
        return_discount += hRow[db.sm_invoice_head.ret_dist_discount.sum()]

    invRecords = qset((db.sm_invoice.cid == c_id) & (db.sm_invoice.depot_id == req_depot) & (
                db.sm_invoice_head.sl == db.sm_invoice.sl)).select(db.sm_invoice.item_id, db.sm_invoice.batch_id,
                                                                   db.sm_invoice.actual_tp, db.sm_invoice.price,
                                                                   db.sm_invoice.item_vat, db.sm_invoice.quantity.sum(),
                                                                   groupby=db.sm_invoice.item_id | db.sm_invoice.batch_id | db.sm_invoice.actual_tp | db.sm_invoice.price | db.sm_invoice.item_vat)
    for invRow in invRecords:
        actualTp = invRow.sm_invoice.actual_tp
        itemRate = invRow.sm_invoice.price
        itemQty = invRow[db.sm_invoice.quantity.sum()]
        itemVat = invRow.sm_invoice.item_vat

        actual_total_tp += actualTp * itemQty
        vatTotal += itemVat * itemQty

        spDiscount =0# (actualTp - itemRate) * itemQty
        totalSpDiscount += spDiscount

    # ----------
    records = qset((db.sm_invoice.cid == c_id) & (db.sm_invoice.depot_id == req_depot) & (
                db.sm_invoice_head.sl == db.sm_invoice.sl)).select(db.sm_invoice.item_id, db.sm_invoice.item_name.max(),
                                                                   db.sm_invoice.batch_id, db.sm_invoice.quantity.sum(),
                                                                   db.sm_invoice.bonus_qty.sum(),
                                                                   db.sm_invoice.return_qty.sum(),
                                                                   db.sm_invoice.return_bonus_qty.sum(),
                                                                   orderby=db.sm_invoice.item_name | db.sm_invoice.batch_id,
                                                                   groupby=db.sm_invoice.item_id | db.sm_invoice.batch_id)

    if len(records)==0:
        response.flash='Data not available'
    # -------------------------
    return dict(records=records, maxMarketID=maxMarketID, maxmarketName=maxmarketName, paymentMode=paymentMode,
                creditType=creditType, search_from_sl=search_from_sl, search_to_sl=search_to_sl,
                territory_id=territory_id, territory_name=territory_name, invoice_dateFrom=invoice_dateFrom,
                invoice_dateTo=invoice_dateTo, d_man_id=d_man_id, d_man_name=d_man_name, clientCount=clientCount,
                invoiceTotal=invoiceTotal, actual_total_tp=actual_total_tp,ret_actual_total_tp=ret_actual_total_tp, return_sp_discount=return_sp_discount,
                totalAmount=totalAmount, vatTotal=vatTotal, totalDiscount=totalDiscount,
                totalSpDiscount=totalSpDiscount, return_tp=return_tp, return_vat=return_vat,
                return_discount=return_discount,dist_id=dist_id,dist_name=dist_name,depot_id=depot_id,depot_name=depot_name,toDate=toDate,dist_disc_percent=dist_disc_percent)
