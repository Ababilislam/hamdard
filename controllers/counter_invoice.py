  

def counter_invoice_show():  

    if ((session.cid==None) or (session.cid=='None')):
        redirect(URL('default','index'))
    response.title='Counter Invoice'
    c_id=session.cid
    user_type = session.user_type

    depot_ID=str(request.vars.depot_ID).strip().replace('None','')
    from_dt=str(request.vars.from_dt).strip().replace('None','')
    to_dt=str(request.vars.to_dt).strip().replace('None','')
    sl=str(request.vars.sl).strip().replace('None','')
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
    session.sl = sl
    session.discount_type = discount_type
    session.physician_id = physician_id
    filter_button = str(request.vars.btn_filter).strip()
    all_button = str(request.vars.btn_all).strip()
    counter_condition=''

#=============================== PAGING ===================================
    if len(request.args):
        page_Number = int(request.args[0])
    else:
        page_Number = 0

    item_per_page = 20

    if page_Number is not None and item_per_page is not None:
        limit_by = (page_Number * item_per_page, (page_Number + 1) * item_per_page + 1)

#============================== PAGING =====================================

    
    if filter_button == "Filter":
        session.depot_ID = depot_ID
        session.depot_name = depot_name

        if session.depot_ID != '':
            counter_condition = counter_condition+" and depot_id = '"+str(depot_ID)+"'"

        if ((session.from_dt!='') and (session.to_dt!='')):
            counter_condition = counter_condition+" and invoice_date >= '"+str(session.from_dt)+"' and invoice_date <= '"+str(session.to_dt)+"'"

        if session.sl != '':
            counter_condition = counter_condition+" and order_sl_counter = '"+str(session.sl)+"'"

        if session.discount_type != '':
            counter_condition = counter_condition+" and discount_type = '"+str(session.discount_type)+"'"

        if session.physician_id != '':
            physician_ID =str(session.physician_id).split('|')[0]
            counter_condition = counter_condition+" and physician_id = '"+str(physician_ID)+"'"
       
    if all_button == "All":
        counter_condition = ""
        session.filter_button = None
        session.depot_ID = ""
        session.depot_name = ""
        session.from_dt = ""
        session.to_dt = ""
        session.sl = ""
        session.discount_type = ""
        session.physician_id = ""

    if user_type == 'Admin':
        counter_invoiceRows_sql = "SELECT * from sm_invoice_head_counter where cid = '"+c_id+"' "+ counter_condition+" AND status = 'Invoiced' group by order_sl_counter,depot_id order by order_datetime desc, order_sl_counter desc limit %d, %d" % limit_by
        counter_invoiceRows = db.executesql(counter_invoiceRows_sql, as_dict=True)

        get_total_record_count_sql = "SELECT * from sm_invoice_head_counter where cid = '"+c_id+"' "+ counter_condition+" AND status = 'Invoiced' group by order_sl_counter,depot_id order by order_datetime desc, order_sl_counter desc "
        get_total_record_count = db.executesql(get_total_record_count_sql, as_dict=True)

    elif user_type == 'Depot':
        depot_id=session.depot_id
        counter_invoiceRows_sql = "SELECT * from sm_invoice_head_counter where cid = '"+c_id+"' "+ counter_condition+" and depot_id ='"+str(depot_id)+"' AND status = 'Invoiced' group by order_sl_counter order by order_datetime desc, order_sl_counter desc limit %d, %d" % limit_by
        counter_invoiceRows = db.executesql(counter_invoiceRows_sql, as_dict=True)

        get_total_record_count_sql = "SELECT * from sm_invoice_head_counter where cid = '"+c_id+"' "+ counter_condition+" and depot_id ='"+str(depot_id)+"' AND status = 'Invoiced' group by order_sl_counter order by order_datetime desc, order_sl_counter desc "
        get_total_record_count = db.executesql(get_total_record_count_sql, as_dict=True)

    session.counter_condition = counter_condition

    
    return dict(counter_invoiceRows=counter_invoiceRows, page_Number=page_Number, item_per_page = item_per_page, get_total_record_count = get_total_record_count)



#======================================= COUNTER INVOICE DETAILS =====================================#

def counter_invoice_details():
    c_id = session.cid
    sl = request.args(0)
    depot_id = request.args(1)
    
    counter_invoice_details_Rows_sql = "SELECT * from sm_invoice_counter where cid = '"+c_id+"' and order_sl_counter =  "+sl+" and depot_id =  '"+str(depot_id)+"' group by depot_id,item_id ;"
    counter_invoice_details_Rows = db.executesql(counter_invoice_details_Rows_sql, as_dict=True)
    
    return dict(counter_invoice_details_Rows= counter_invoice_details_Rows)



#======================================= COUNTER INVOICE LIST DOWNLOAD =====================================#

def counter_invoice_list_Download():
    c_id = session.cid

    user_type = session.user_type
    if user_type == 'Admin':
        counter_invoiceRows_sql = "SELECT * from sm_invoice_head_counter where cid = '"+c_id+"' "+session.counter_condition+" AND status = 'Invoiced' group by depot_id, order_sl_counter order by order_sl_counter desc;"
        counter_invoiceRows = db.executesql(counter_invoiceRows_sql, as_dict=True)

    elif user_type == 'Depot':
        depot_id=session.depot_id
        counter_invoiceRows_sql = "SELECT * from sm_invoice_head_counter where cid = '"+c_id+"' "+session.counter_condition+" AND status = 'Invoiced' and depot_id ='"+str(depot_id)+"' group by depot_id,order_sl_counter order by order_sl_counter desc;"
        counter_invoiceRows = db.executesql(counter_invoiceRows_sql, as_dict=True)

    myString = 'Counter Invoice List\n\n'
    myString += 'Invoice SL, Depot ID, Depot Name, Pysician ID, Physician Name, Discount Type, Invoice Date, Status, Actual TP, Discount, Total Amount\n'
    total=0
    attTime = ''
    totalCount = 0
    for i in range(len(counter_invoiceRows)):
        records_ov_dict=counter_invoiceRows[i]   
        record_id=str(records_ov_dict["id"])
        sl=str(records_ov_dict["order_sl_counter"])
        depot_id=str(records_ov_dict["depot_id"]) 
        depot_name=str(records_ov_dict["depot_name"])
        physician_id=str(records_ov_dict["physician_id"])
        physician_name=str(records_ov_dict["physician_name"])
        discount_type=str(records_ov_dict["discount_type"])                                         
        order_datetime=str(records_ov_dict["order_datetime"])
        status=str(records_ov_dict["status"])
        actual_total_tp=records_ov_dict["actual_total_tp"]
        discount= records_ov_dict["discount"]
        total_amount= records_ov_dict["total_amount"]
        
        myString += str(sl) + ',' + str(depot_id) + ',' + str(depot_name) + ',' + str(physician_id) + ',' + str(physician_name) + ',' + str(discount_type) + ',' + str(order_datetime) + ',' + str(status) + ',' + str(actual_total_tp) + ',' + str(discount) + ',' + str(total_amount) + '\n'

    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=counter_invoice_list.csv'
    return str(myString)



#======================================= COUNTER INVOICE PRINT =====================================#

def counter_invoice_print():
    c_id = session.cid
    sl_num = request.args(0)
    depot_id = request.args(1)
    
    counter_invoice_details_rows_print_sql = "SELECT * from sm_invoice_counter where cid = '"+c_id+"' and order_sl_counter =  "+sl_num+" and depot_id =  '"+str(depot_id)+"' group by order_sl_counter, depot_id, item_id ;"
    counter_invoice_details_rows_print = db.executesql(counter_invoice_details_rows_print_sql, as_dict=True)

    counter_invoice_head_rows_print_sql = "SELECT * from sm_invoice_head_counter where cid = '"+c_id+"' and order_sl_counter =  "+sl_num+" and depot_id =  '"+str(depot_id)+"' group by order_sl_counter, depot_id  ;"
    counter_invoice_head_rows_print = db.executesql(counter_invoice_head_rows_print_sql, as_dict=True)


    for i in range(len(counter_invoice_head_rows_print)):
        records_ov_dict=counter_invoice_head_rows_print[i]   
        record_id=str(records_ov_dict["id"])
        sl=str(records_ov_dict["order_sl_counter"])
        depot_id=str(records_ov_dict["depot_id"]) 
        depot_name=str(records_ov_dict["depot_name"])
        physician_id=str(records_ov_dict["physician_id"])
        physician_name=str(records_ov_dict["physician_name"])
        discount_type=str(records_ov_dict["discount_type"])
        status=str(records_ov_dict["status"])
        note=str(records_ov_dict["note"])
        customer_id=str(records_ov_dict["customer_id"])
        customer_name=str(records_ov_dict["customer_name"])
        phone=str(records_ov_dict["phone"])
        gender=str(records_ov_dict["gender"])
        age=str(records_ov_dict["age"])
        customer_category=str(records_ov_dict["customer_category"])
        staff_id=str(records_ov_dict["staff_id"])
    
    return dict(counter_invoice_details_rows_print=counter_invoice_details_rows_print, sl=sl, depot_id=depot_id, depot_name=depot_name, physician_id=physician_id, physician_name=physician_name, discount_type=discount_type, status=status, note=note, customer_id=customer_id, customer_name=customer_name, phone=phone, gender=gender, age=age, customer_category=customer_category, staff_id=staff_id)



#======================================= COUNTER INVOICE RETURN =====================================#

def counter_invoice_return():
    response.title='Counter Return'
    c_id = session.cid
    depot_id = session.depot_id
    sl_num = request.args(0)
    from datetime import datetime
    current_datetime = date_fixed
    current_date = str(current_datetime).split(' ')[0]
    status = 'Return'
    return_sl = 0

    return_sl_generator_sql = "SELECT id,return_sl FROM invoice_head_counter_return WHERE cid='" + c_id + "' AND depot_id='"+str(depot_id)+"'  ORDER BY id desc LIMIT 1;"
    return_sl_generator = db.executesql(return_sl_generator_sql, as_dict=True)
    
    for sl in range(len(return_sl_generator)):
        return_sl_RecordsStr = return_sl_generator[sl]
        row_id = str(return_sl_RecordsStr['id'])
        return_sl = int(return_sl_RecordsStr['return_sl']) + 1

    get_counter_invoice_head_sql = "SELECT * FROM sm_invoice_head_counter where cid = '"+c_id+"' AND depot_id = '"+str(depot_id)+"' AND order_sl_counter = '"+str(sl_num)+"' GROUP BY order_sl_counter ;"
    get_counter_invoice_head_record = db.executesql(get_counter_invoice_head_sql, as_dict = True)

    for records in range(len(get_counter_invoice_head_record)):
        item_record = get_counter_invoice_head_record[records]
        order_sl_counter = item_record['order_sl_counter']
        depot_id = str(item_record['depot_id'])
        depot_name = str(item_record['depot_name'])
        physician_id = str(item_record['physician_id'])
        physician_name = str(item_record['physician_name'])
        discount_type = str(item_record['discount_type'])
        invoice_date = str(item_record['invoice_date'])
        ym_date = str(item_record['ym_date'])
        actual_total_tp = str(item_record['actual_total_tp'])
        total_amount = str(item_record['total_amount'])
        discount = str(item_record['discount'])
        note = str(item_record['note'])
        customer_id = str(item_record['customer_id'])
        phone = str(item_record['phone'])
        customer_name = str(item_record['customer_name'])
        gender = str(item_record['gender'])
        age = str(item_record['age'])
        customer_category = str(item_record['customer_category'])
        staff_id = str(item_record['staff_id'])

        insert_invoice_head_counter_return_sql = "INSERT INTO invoice_head_counter_return (cid, depot_id, depot_name, order_sl_counter, return_sl,  return_date, return_datetime, physician_id, physician_name, discount_type, status, actual_total_tp, total_amount, discount, invoice_date, ym_date, note, customer_id, phone, customer_name, gender, age, customer_category, staff_id) VALUES ('"+str(c_id)+"','"+str(depot_id)+"','"+str(depot_name)+"','"+str(order_sl_counter)+"', '"+str(return_sl)+"','"+str(current_date)+"', '"+str(current_datetime)+"', '"+str(physician_id)+"','"+str(physician_name)+"','"+str(discount_type)+"', '"+str(status)+"', '"+str(actual_total_tp)+"', '"+str(total_amount)+"', '"+str(discount)+"', '"+str(invoice_date)+"', '"+str(ym_date)+"','"+str(note)+"', '"+str(customer_id)+"','"+str(phone)+"','"+str(customer_name)+"','"+str(gender)+"','"+str(age)+"','"+str(customer_category)+"','"+str(staff_id)+"');" 
        insert_sm_invoice_head_counter = db.executesql(insert_invoice_head_counter_return_sql)

        update_status_invoice_head_counter_sql = "UPDATE sm_invoice_head_counter SET status = '"+str(status)+"' WHERE cid = '"+c_id+"' AND depot_id = '"+str(depot_id)+"' AND order_sl_counter = '"+str(sl_num)+"' limit 1 ;"
        update_status_invoice_head_counter = db.executesql(update_status_invoice_head_counter_sql)

        update_status_order_head_counter_sql = "UPDATE sm_order_head_counter SET status = '"+str(status)+"' WHERE cid = '"+c_id+"' AND depot_id = '"+str(depot_id)+"' AND order_sl_counter = '"+str(sl_num)+"' limit 1 ;"
        update_status_order_head_counter = db.executesql(update_status_order_head_counter_sql)

    get_counter_invoice_sql = "SELECT * FROM sm_invoice_counter where cid = '"+c_id+"' AND depot_id = '"+str(depot_id)+"' AND order_sl_counter = '"+str(sl_num)+"' GROUP BY item_id ;"
    get_counter_invoice_record = db.executesql(get_counter_invoice_sql, as_dict = True)

    for item_record in range(len(get_counter_invoice_record)):
        invoice_item_record = get_counter_invoice_record[item_record]
        order_sl_counter = invoice_item_record['order_sl_counter']
        depot_id = str(invoice_item_record['depot_id'])
        depot_name = str(invoice_item_record['depot_name'])
        physician_id = str(invoice_item_record['physician_id'])
        physician_name = str(invoice_item_record['physician_name'])
        discount_type = str(invoice_item_record['discount_type'])
        invoice_date = str(invoice_item_record['invoice_date'])
        item_id = str(invoice_item_record['item_id'])
        item_name = str(invoice_item_record['item_name'])
        quantity = str(invoice_item_record['quantity'])
        actual_tp = str(invoice_item_record['actual_tp'])
        total_price = str(invoice_item_record['total_price'])
        item_discount_percent = str(invoice_item_record['item_discount_percent'])

        insert_invoice_counter_return_sql = "INSERT INTO invoice_counter_return (cid, depot_id, depot_name, order_sl_counter, return_sl, return_date, return_datetime, physician_id, physician_name, discount_type, status, actual_tp, total_price, item_discount_percent, invoice_date, item_id, item_name, quantity) VALUES ('"+str(c_id)+"','"+str(depot_id)+"','"+str(depot_name)+"','"+str(order_sl_counter)+"', '"+str(return_sl)+"', '"+str(current_date)+"', '"+str(current_datetime)+"', '"+str(physician_id)+"', '"+str(physician_name)+"', '"+str(discount_type)+"', '"+str(status)+"', '"+str(actual_tp)+"', '"+str(total_price)+"', '"+str(item_discount_percent)+"', '"+str(invoice_date)+"', '"+str(item_id)+"', '"+str(item_name)+"', '"+str(quantity)+"');" 
        insert_sm_invoice_counter = db.executesql(insert_invoice_counter_return_sql)

        update_sm_depot_stock_balance_sql = " UPDATE sm_depot_stock_balance Set counter_qty = counter_qty + '"+str(quantity)+"' WHERE cid ='"+c_id+"' AND depot_id ='"+str(depot_id)+"' AND item_id = '"+str(item_id)+"' and store_name ='Commercial' ; "  
        update_sm_depot_stock_balance = db.executesql(update_sm_depot_stock_balance_sql)

        update_status_invoice_counter_sql = "UPDATE sm_invoice_counter SET status = '"+str(status)+"' WHERE cid = '"+c_id+"' AND depot_id = '"+str(depot_id)+"' AND order_sl_counter = '"+str(sl_num)+"';"
        update_status_invoice_counter = db.executesql(update_status_invoice_counter_sql)

        update_status_order_counter_sql = "UPDATE sm_order_counter SET status = '"+str(status)+"' WHERE cid = '"+c_id+"' AND depot_id = '"+str(depot_id)+"' AND order_sl_counter = '"+str(sl_num)+"';"
        update_status_order_counter = db.executesql(update_status_order_counter_sql)

    session.flash = 'Item Return Successfully'
    redirect(URL('counter_invoice', 'counter_invoice_show'))
    return dict()

