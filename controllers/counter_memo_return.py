                   
#======================================= COUNTER MEMO RETURN LIST SHOW =====================================#

def counter_memo_return_list():  

    if ((session.cid==None) or (session.cid=='None')):
        redirect(URL('default','index'))
    response.title='Memo Return'
    c_id=session.cid
    user_type = session.user_type
    depot_ID=str(request.vars.depot_ID).strip().replace('None','')
    from_dt=str(request.vars.from_dt).strip().replace('None','')
    to_dt=str(request.vars.to_dt).strip().replace('None','')
    sl=str(request.vars.sl).strip().replace('None','')
    return_sl=str(request.vars.return_sl).strip().replace('None','')
    discount_type=str(request.vars.discount_type).strip().replace('None','')
    physician_id=str(request.vars.physician_id).strip().replace('None','')
    try:
        depot_ID = str(request.vars.depot_ID).split('|')[0]
        depot_name = str(request.vars.depot_ID).split('|')[1]
    except:
        depot_ID = ''
        depot_name = ''

    session.from_dt = from_dt
    session.to_dt = to_dt
    session.return_sl = return_sl
    session.sl = sl
    session.discount_type = discount_type
    session.physician_id = physician_id
    filter_button = str(request.vars.btn_filter).strip()
    all_button = str(request.vars.btn_all).strip()
    counter_return_condition=''

#=============================== PAGING ===================================
    if len(request.args):
        page_Number = int(request.args[0])
        # return page
    else:
        page_Number = 0

    item_per_page = 20

    if page_Number is not None and item_per_page is not None:

        # limit_by = ((page_Number + 1) * item_per_page , item_per_page )
        limit_by = (page_Number * item_per_page, (page_Number + 1) * item_per_page + 1)

#============================== PAGING =====================================

    
    if filter_button == "Filter":
        session.depot_ID = depot_ID
        session.depot_name = depot_name

        if session.depot_ID != '':
            counter_return_condition = counter_return_condition+" and depot_id = '"+str(depot_ID)+"'"

        if ((session.from_dt!='') and (session.to_dt!='')):
            counter_return_condition = counter_return_condition+" and invoice_date >= '"+str(session.from_dt)+"' and invoice_date <= '"+str(session.to_dt)+"'"

        # if session.sl != '':
        #     counter_return_condition = counter_return_condition+" and order_sl_counter = '"+str(session.sl)+"'"

        if session.return_sl != '':
            counter_return_condition = counter_return_condition+" and return_sl = '"+str(session.return_sl)+"'"

        if session.discount_type != '':
            counter_return_condition = counter_return_condition+" and discount_type = '"+str(session.discount_type)+"'"

        if session.physician_id != '':
            physician_ID =str(session.physician_id).split('|')[0]
            counter_return_condition = counter_return_condition+" and physician_id = '"+str(physician_ID)+"'"
       
    if all_button == "All":
        counter_return_condition = ""
        session.filter_button = None
        session.depot_ID = ""
        session.depot_name = ""
        session.from_dt = ""
        session.to_dt = ""
        session.sl = ""
        session.return_sl = ""
        session.discount_type = ""
        session.physician_id = ""

    if user_type == 'Admin':
        counter_return_head_Rows_sql = "SELECT * from invoice_head_counter_return where cid = '"+c_id+"' "+ counter_return_condition+" AND status = 'Return' group by return_sl, depot_id order by return_sl desc limit %d, %d" % limit_by
        counter_return_head_Rows = db.executesql(counter_return_head_Rows_sql, as_dict=True)

        get_total_record_count_sql = "SELECT * from invoice_head_counter_return where cid = '"+c_id+"' "+ counter_return_condition+" AND status = 'Return' group by return_sl, depot_id  order by return_sl desc "
        get_total_record_count = db.executesql(get_total_record_count_sql, as_dict=True)

    elif user_type == 'Depot':
        depot_id=session.depot_id
        counter_return_head_Rows_sql = "SELECT * from invoice_head_counter_return where cid = '"+c_id+"' "+ counter_return_condition+" and depot_id ='"+str(depot_id)+"' AND status = 'Return' group by return_sl, depot_id order by return_sl desc limit %d, %d" % limit_by
        counter_return_head_Rows = db.executesql(counter_return_head_Rows_sql, as_dict=True)

        get_total_record_count_sql = "SELECT * from invoice_head_counter_return where cid = '"+c_id+"' "+ counter_return_condition+" and depot_id ='"+str(depot_id)+"' AND status = 'Return' group by return_sl, depot_id order by return_sl desc "
        get_total_record_count = db.executesql(get_total_record_count_sql, as_dict=True)

    session.counter_return_condition = counter_return_condition

    
    return dict(counter_return_head_Rows=counter_return_head_Rows, page_Number=page_Number, item_per_page = item_per_page, get_total_record_count = get_total_record_count)



#======================================= COUNTER MEMO RETURN ITEM DETAILS =====================================#

def counter_memo_return_details():
    c_id = session.cid
    return_sl = request.args(0)
    depot_id = request.args(1)
    # return return_sl
    
    counter_return_details_Rows_sql = "SELECT * from invoice_counter_return where cid = '"+c_id+"' and return_sl =  "+return_sl+" and depot_id ='"+str(depot_id)+"' group by depot_id,item_id ;"
    # return counter_return_details_Rows_sql
    counter_details_details_Rows = db.executesql(counter_return_details_Rows_sql, as_dict=True)
    
    return dict(counter_details_details_Rows= counter_details_details_Rows)



#======================================= COUNTER MEMO RETURN LIST DOWNLOAD =====================================#

def counter_memo_return_list_Download():
    c_id = session.cid
    user_type = session.user_type
    counter_return_condition = session.counter_return_condition
    # return counter_return_condition
    if user_type == 'Admin':
        counter_memo_Rows_sql = "SELECT * from invoice_head_counter_return where cid = '"+c_id+"' "+counter_return_condition+" AND status = 'Return' group by return_sl order by return_sl desc;"
        counter_memo_Rows = db.executesql(counter_memo_Rows_sql, as_dict=True)

    elif user_type == 'Depot':
        depot_id=session.depot_id
        counter_memo_Rows_sql = "SELECT * from invoice_head_counter_return where cid = '"+c_id+"' "+counter_return_condition+" AND status = 'Return' and depot_id ='"+str(depot_id)+"' group by return_sl order by return_sl desc;"
        # return counter_memo_Rows_sql
        counter_memo_Rows = db.executesql(counter_memo_Rows_sql, as_dict=True)

    # return counter_memo_Rows
    myString = 'Memo Return List\n\n'
    myString += 'Return SL, Depot ID, Depot Name, Pysician ID, Physician Name, Discount Type, Return Date, Status, Actual TP, Discount, Total Amount\n'
    total=0
    attTime = ''
    totalCount = 0
    for i in range(len(counter_memo_Rows)):
        records_ov_dict=counter_memo_Rows[i]   
        record_id=str(records_ov_dict["id"])
        return_sl=str(records_ov_dict["return_sl"])
        depot_id=str(records_ov_dict["depot_id"]) 
        depot_name=str(records_ov_dict["depot_name"])
        physician_id=str(records_ov_dict["physician_id"])
        physician_name=str(records_ov_dict["physician_name"])
        discount_type=str(records_ov_dict["discount_type"])                                         
        return_datetime=str(records_ov_dict["return_datetime"])
        status=str(records_ov_dict["status"])
        actual_total_tp=records_ov_dict["actual_total_tp"]
        discount= records_ov_dict["discount"]
        total_amount= records_ov_dict["total_amount"]
        
        myString += str(return_sl) + ',' + str(depot_id) + ',' + str(depot_name) + ',' + str(physician_id) + ',' + str(physician_name) + ',' + str(discount_type) + ',' + str(return_datetime) + ',' + str(status) + ',' + str(actual_total_tp) + ',' + str(discount) + ',' + str(total_amount) + '\n'

    # Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=counter_memo_return_list.csv'
    return str(myString)


