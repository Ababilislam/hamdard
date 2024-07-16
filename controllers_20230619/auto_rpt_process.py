import time


# inv discount update
#http://127.0.0.1:8000/hamdard/auto_rpt_process/process_discount?req_date=
def process_discount():
    cid = 'HAMDARD'
    req_date=request.vars.req_date

    db.executesql("TRUNCATE z_temp_inv_head_disc_fix;")

    insetSql = "insert into `z_temp_inv_head_disc_fix` (`cid`, `depot_id`, `sl`, `total_amount_new`, `discount_new`,`disc_diff`) SELECT cid,`depot_id`,sl,actual_total_tp-(`actual_total_tp`*.15) as total_amount_new,(`actual_total_tp`*.15) as discount_new,(`discount`-(`actual_total_tp`*.15)) as disc_diff FROM `sm_invoice_head` WHERE cid='"+cid+"' and status='Invoiced' and invoice_date='"+req_date+"' group by `depot_id`, `sl` HAVING disc_diff>0;"
    insetSql = db.executesql(insetSql)

    updateSql = "update `sm_invoice_head` a,z_temp_inv_head_disc_fix b set a.total_amount=b.total_amount_new,a.discount=b.discount_new WHERE  a.cid=b.cid and a.depot_id=b.depot_id and a.sl=b.sl;"
    updateSql = db.executesql(updateSql)

    updateSql1 = "update `sm_invoice` a,z_temp_inv_head_disc_fix b set a.discount=b.discount_new WHERE a.cid=b.cid and a.depot_id=b.depot_id and a.sl=b.sl;"
    updateSql1 = db.executesql(updateSql1)


    return 'Done '+str(req_date)



#http://127.0.0.1:8000/hamdard/auto_rpt_process/process_inv_to_rpt

def process_inv_to_rpt():
    cid='HAMDARD'

    sqlInvRow="SELECT id,cid,depot_id,sl,invoice_date,posted_by,posted_on FROM `sm_invoice_head` where cid='"+cid+"' and status='Invoiced' and rpt_trans_flag=0 limit 0,20"
    sqlInvRow=db.executesql(sqlInvRow,as_dict=True)

    if len(sqlInvRow)==0:
        return 'Done All '+str(req_date)
    else:
        for i in range(len(sqlInvRow)):
            sqlInvRowS=sqlInvRow[i]
            c_id=sqlInvRowS['cid']
            req_depot = sqlInvRowS['depot_id']
            req_sl = sqlInvRowS['sl']
            req_date = sqlInvRowS['invoice_date'] #current_date
            created_by = sqlInvRowS['posted_by']
            created_on = sqlInvRowS['posted_on']


            # -------------------------------- Loop start
            headRow = db((db.sm_invoice_head.cid==c_id)& (db.sm_invoice_head.depot_id==req_depot) & (db.sm_invoice_head.sl==req_sl)& (db.sm_invoice_head.status=='Invoiced')).select(
                db.sm_invoice_head.id, db.sm_invoice_head.sl, db.sm_invoice_head.d_man_id, db.sm_invoice_head.d_man_name,
                db.sm_invoice_head.shipment_no, db.sm_invoice_head.order_sl, db.sm_invoice_head.updated_by,
                db.sm_invoice_head.depot_id, db.sm_invoice_head.store_id, db.sm_invoice_head.client_id,
                db.sm_invoice_head.area_id, db.sm_invoice_head.discount, db.sm_invoice_head.sp_discount,
                db.sm_invoice_head.depot_name, db.sm_invoice_head.store_name, db.sm_invoice_head.delivery_date,
                db.sm_invoice_head.payment_mode, db.sm_invoice_head.credit_note, db.sm_invoice_head.client_name,
                db.sm_invoice_head.rep_id, db.sm_invoice_head.rep_name, db.sm_invoice_head.market_id,
                db.sm_invoice_head.market_name, db.sm_invoice_head.level0_id, db.sm_invoice_head.level0_name,
                db.sm_invoice_head.level1_id, db.sm_invoice_head.level1_name, db.sm_invoice_head.level2_id,
                db.sm_invoice_head.level2_name, db.sm_invoice_head.area_name, db.sm_invoice_head.note,
                db.sm_invoice_head.posted_by,db.sm_invoice_head.d_man_id,db.sm_invoice_head.d_man_name,db.sm_invoice_head.cl_category_id,db.sm_invoice_head.cl_category_name,db.sm_invoice_head.cl_sub_category_id,db.sm_invoice_head.cl_sub_category_name,db.sm_invoice_head.client_limit_amt,db.sm_invoice_head.total_amount,db.sm_invoice_head.actual_total_tp,db.sm_invoice_head.vat_total_amount,db.sm_invoice_head.discount,db.sm_invoice_head.sp_discount,db.sm_invoice_head.shipment_no, limitby=(0, 1))
            if not headRow:
                errorStr = 'Invalid SL no ' + str(req_rowid)
            else:
                inv_rowid = headRow[0].id
                store_id = headRow[0].store_id
                client_id = headRow[0].client_id
                area_id = headRow[0].area_id

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

                d_man_id = headRow[0].d_man_id
                d_man_name = headRow[0].d_man_name

                cl_category_id = headRow[0].cl_category_id
                cl_category_name = headRow[0].cl_category_name
                cl_sub_category_id = headRow[0].cl_sub_category_id
                cl_sub_category_name = headRow[0].d_man_id

                client_limit_amt = headRow[0].client_limit_amt

                total_amount = headRow[0].total_amount
                actual_total_tp = headRow[0].actual_total_tp
                vat_total_amount = headRow[0].vat_total_amount
                discount = headRow[0].discount
                sp_discount = headRow[0].sp_discount
                shipment_no = headRow[0].shipment_no


                totalAmount = total_amount
                actual_total_tp = actual_total_tp
                total_vat_amount = vat_total_amount
                discount = discount
                sp_discount = sp_discount


                # ----------------------- Report Transaction ***
                transaction_date = req_date



                insertRpt = db.sm_rpt_transaction.insert(cid=c_id, depot_id=req_depot, depot_name=depot_name,
                                                         store_id=store_id, store_name=store_name, inv_rowid=inv_rowid,
                                                         inv_sl=req_sl, invoice_date=req_date, transaction_type='INV',
                                                         transaction_date=transaction_date, transaction_ref=req_sl,
                                                         transaction_ref_date=req_date, trans_net_amt=totalAmount,
                                                         tp_amt=actual_total_tp, vat_amt=total_vat_amount,
                                                         disc_amt=round(discount, 2), spdisc_amt=sp_discount,
                                                         adjust_amount=0, delivery_date=delivery_date,
                                                         payment_mode=payment_mode, credit_note=credit_note,
                                                         client_id=client_id, client_name=client_name,
                                                         cl_category_id=cl_category_id, cl_category_name=cl_category_name,
                                                         cl_sub_category_id=cl_sub_category_id,
                                                         cl_sub_category_name=cl_sub_category_name,
                                                         client_limit_amt=client_limit_amt, rep_id=rep_id,
                                                         rep_name=rep_name, market_id=market_id, market_name=market_name,
                                                         d_man_id=d_man_id, d_man_name=d_man_name, level0_id=level0_id,
                                                         level0_name=level0_name, level1_id=level1_id,
                                                         level1_name=level1_name, level2_id=level2_id,
                                                         level2_name=level2_name, area_id=area_id, area_name=area_name,
                                                         shipment_no=shipment_no, note=note, created_by=posted_by,created_on=created_on)

                headRow[0].update_record(rpt_trans_flag=1)

    return 'Done1'


#http://127.0.0.1:8000/hamdard/auto_rpt_process/process_ret_to_rpt

def process_ret_to_rpt():
    cid='HAMDARD'

    sqlRetRow="SELECT id,cid,depot_id,sl,return_date,invoice_sl,returned_on,returned_by FROM `sm_return_head` where cid='"+cid+"' and status='Returned' and rpt_trans_flag=0 limit 0,5"
    sqlRetRow=db.executesql(sqlRetRow,as_dict=True)

    if len(sqlRetRow)==0:
        return 'Done All'
    else:
        for i in range(len(sqlRetRow)):
            sqlRetRowS=sqlRetRow[i]
            c_id=sqlRetRowS['cid']
            req_depot = sqlRetRowS['depot_id']
            req_sl = sqlRetRowS['sl']
            invoiceSl = sqlRetRowS['invoice_sl']
            req_date = sqlRetRowS['return_date'] #current_date

            created_by = sqlRetRowS['returned_by']
            created_on = sqlRetRowS['returned_on']

            headRow = db((db.sm_return_head.cid == c_id) & (db.sm_return_head.depot_id == req_depot) & (
                        db.sm_return_head.sl == req_sl)).select(db.sm_return_head.ALL, limitby=(0, 1))
            if headRow:

                # ------------------------
                store_id = headRow[0].store_id
                area_id = headRow[0].area_id
                depot_name = headRow[0].depot_name
                store_name = headRow[0].store_name
                client_id = headRow[0].client_id
                client_name = headRow[0].client_name

                rep_id = headRow[0].rep_id
                rep_name = headRow[0].rep_name
                market_id = headRow[0].market_id
                market_name = headRow[0].market_name
                shipment_no = headRow[0].shipment_no
                invoice_date = headRow[0].invoice_date
                d_man_id = headRow[0].d_man_id
                d_man_name = headRow[0].d_man_name

                level0_id = headRow[0].level0_id
                level0_name = headRow[0].level0_name
                level1_id = headRow[0].level1_id
                level1_name = headRow[0].level1_name
                level2_id = headRow[0].level2_id
                level2_name = headRow[0].level2_name
                area_name = headRow[0].area_name

                cl_category_id = headRow[0].cl_category_id
                cl_category_name = headRow[0].cl_category_name
                cl_sub_category_id = headRow[0].cl_sub_category_id
                cl_sub_category_name = headRow[0].cl_sub_category_name

                note = headRow[0].note

                total_amount = headRow[0].total_amount
                ret_actual_total_tp = headRow[0].ret_actual_total_tp
                vat_total_amount = headRow[0].vat_total_amount
                discount = headRow[0].discount
                sp_discount = headRow[0].sp_discount
                shipment_no = headRow[0].shipment_no

                totalAmount = total_amount
                ret_actual_total_tp = ret_actual_total_tp
                total_vat_amount = vat_total_amount
                discount = discount
                total_ret_sp_amount = sp_discount

                inv_rowid=0
                delivery_date = ''
                payment_mode = ''
                credit_note = ''
                client_limit_amt = 0
                invHRow = db((db.sm_invoice_head.cid == c_id) & (
                        db.sm_invoice_head.depot_id == req_depot) & (
                                     db.sm_invoice_head.sl == invoiceSl)).select(
                    db.sm_invoice_head.id,
                    db.sm_invoice_head.delivery_date,
                    db.sm_invoice_head.payment_mode, db.sm_invoice_head.credit_note,
                    db.sm_invoice_head.client_limit_amt, limitby=(0, 1))
                if invHRow:
                    inv_rowid = invHRow[0].id
                    delivery_date = invHRow[0].delivery_date
                    payment_mode = invHRow[0].payment_mode
                    credit_note = invHRow[0].credit_note
                    client_limit_amt = invHRow[0].client_limit_amt

                # ----------------------- Report Transaction ***
                transaction_date = req_date
                insertRpt = db.sm_rpt_transaction.insert(cid=c_id, depot_id=req_depot,
                                                         depot_name=depot_name,
                                                         store_id=store_id,
                                                         store_name=store_name,
                                                         inv_rowid=inv_rowid, inv_sl=invoiceSl,
                                                         invoice_date=invoice_date,
                                                         transaction_type='RET',
                                                         transaction_date=transaction_date,
                                                         transaction_ref=req_sl,
                                                         transaction_ref_date=req_date,
                                                         trans_net_amt=totalAmount * (-1),
                                                         tp_amt=ret_actual_total_tp * (-1),
                                                         vat_amt=total_vat_amount * (-1),
                                                         disc_amt=round(discount, 2) * (-1),
                                                         spdisc_amt=total_ret_sp_amount * (-1),
                                                         adjust_amount=0,
                                                         delivery_date=delivery_date,
                                                         payment_mode=payment_mode,
                                                         credit_note=credit_note,
                                                         client_id=client_id,
                                                         client_name=client_name,
                                                         cl_category_id=cl_category_id,
                                                         cl_category_name=cl_category_name,
                                                         cl_sub_category_id=cl_sub_category_id,
                                                         cl_sub_category_name=cl_sub_category_name,
                                                         client_limit_amt=client_limit_amt,
                                                         rep_id=rep_id, rep_name=rep_name,
                                                         market_id=market_id,
                                                         market_name=market_name,
                                                         d_man_id=d_man_id,
                                                         d_man_name=d_man_name,
                                                         level0_id=level0_id,
                                                         level0_name=level0_name,
                                                         level1_id=level1_id,
                                                         level1_name=level1_name,
                                                         level2_id=level2_id,
                                                         level2_name=level2_name,
                                                         area_id=area_id, area_name=area_name,
                                                         shipment_no=shipment_no, note=note,created_by=created_by,created_on=created_on)


                headRow[0].update_record(rpt_trans_flag=1)

    return 'Done1'


