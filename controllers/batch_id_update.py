def batch_update():
    response.title='Batch_id Update'
    c_id=session.cid
    depot_id = session.depot_id
    submit = request.vars.submit
    update_btn = request.vars.update_btn
    all_update_btn = request.vars.all_update_btn
    total_rec = 0
    check_sl = {}
    if submit:
        inv_sl=request.vars.inv_sl
        session.inv_sl=inv_sl

    if update_btn:
        sl = request.args(0)
        item_id = request.args(1)
        quantity = request.args(2)
        stock_qty = request.args(3)
        batch_id= '1001'
        if int(quantity) > int(stock_qty) :
            session.flash='Stock is not Available'
        else:
            update_batch_sql = "UPDATE sm_invoice SET batch_id = '"+str(batch_id)+"' WHERE cid='"+str(c_id)+"' and depot_id='"+str(depot_id)+"' and sl='"+str(sl)+"' and item_id = '"+str(item_id)+"' limit 1;"
            up_date = db.executesql(update_batch_sql)
            session.flash='Update Successfully!'
            redirect (URL('batch_id_update','batch_update'))

    if all_update_btn:
        sl = request.args(0)
        # quantity = request.args(1)
        # stock_qty = request.args(2)
        # if quantity <= stock_qty :
        batch_id= '1001'
        update_batch_sql = "UPDATE sm_invoice SET batch_id = '"+str(batch_id)+"' WHERE cid='"+str(c_id)+"' and depot_id='"+str(depot_id)+"' and sl='"+str(sl)+"';"
        up_date = db.executesql(update_batch_sql)
        session.flash='Update All Successfully!'
        redirect (URL('batch_id_update','batch_update'))

    inv_sl=session.inv_sl
    total_record_sql = f"SELECT COUNT(id) AS total FROM sm_invoice where cid='"+str(c_id)+"' and depot_id='"+str(depot_id)+"' and sl='"+str(inv_sl)+"' group by depot_id,sl ORDER BY id ASC;"
    total_record = db.executesql(total_record_sql, as_dict = True)

    check_sl_sql = "select * from sm_invoice where cid='"+str(c_id)+"' and depot_id='"+str(depot_id)+"' and sl='"+str(inv_sl)+"' group by depot_id,sl,item_id;"
    check_sl = db.executesql(check_sl_sql, as_dict=True)

    return dict(check_sl=check_sl,total_rec=total_rec, total_record=total_record,inv_sl=inv_sl)

def item_delete():
    c_id = session.cid
    depot_id = session.depot_id
    btn_delete_x = request.args[0]
    delete_sql = "DELETE from sm_invoice where cid = '"+c_id+"' and item_id='"+str(btn_delete_x)+"' and depot_id='"+str(depot_id)+"' ;"
    db.executesql(delete_sql)
    session.flash = 'Deleted Successfully'
    redirect (URL('batch_id_update','batch_update'))
    # return dict()

# def update():
#     # return 10
#     c_id = session.cid
#     depot_id = session.depot_id
#     item_id = request.args[0]
#     batch_id= '1001'
#     # return batch_id
#     if batch_id != '1001':
#         update_sql = "UPDATE sm_invoice SET batch_id = '"+str(batch_id)+"' WHERE item_id = '"+str(item_id)+"' and depot_id='"+str(depot_id)+"';"
#         # return update_sql
#         up_date=db.executesql(update_sql)
#         response.flash='Update Successfully!'
#         redirect (URL('batch_id_update','batch_update'))
    # return dict()
# if update_btn:
# item_id = request.vars.item_id
# update_level_sql = "UPDATE sm_level SET level_name = '"+str(national_name)+"' , level0_name = '"+str(national_name)+"', updated_on = '"+str(current_date_time)+"', updated_by = '"+str(session.user_id)+"' WHERE id = '"+str(item_id)+"' ;"
# db.executesql(update_level_sql)
# response.flash='Update Successfully!'