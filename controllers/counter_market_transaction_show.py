# ================================= COUNTER MARKET TRANSACTION SHOW ============================================ #

def counter_market_transaction_show():  
    from datetime import datetime
    if ((session.cid==None) or (session.cid=='None')):
        redirect(URL('default','index'))
    response.title='Counter Market Transaction Show'
    c_id=session.cid
    user_type = session.user_type
    # depot_id=session.depot_id
    item=str(request.vars.item_id).strip().replace('None','')
    session.item = item
    try:
        item_id = str(request.vars.item_id).split('|')[0]
        item_name = str(request.vars.item_id).split('|')[1]
    except:
        item_id = ''
        item_name = ''
    
    from_dt=str(request.vars.from_dt).strip().replace('None','')
    to_dt=str(request.vars.to_dt).strip().replace('None','')
    session.from_dt = from_dt
    session.to_dt = to_dt
    transaction_type=str(request.vars.transaction_type).strip().replace('None','')
    session.transaction_type = transaction_type
    filter_button = str(request.vars.btn_filter).strip()
    all_button = str(request.vars.btn_all).strip()
    t_condition=''
    date_difference = 0
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
        if ((session.from_dt!='') and (session.to_dt!='')):
            from_dt_datetime = datetime.strptime(session.from_dt, '%Y-%m-%d')
            to_dt_datetime = datetime.strptime(session.to_dt, '%Y-%m-%d') 
            date_difference = (to_dt_datetime - from_dt_datetime).days
            if date_difference > 31:
                session.flash = 'Maximum 31 Days Allow for Date Filter'
                redirect(URL('counter_market_transaction_show','counter_market_transaction_show'))
            else:
                t_condition = t_condition+" and transaction_date >= '"+str(session.from_dt)+"' and transaction_date <= '"+str(session.to_dt)+"'"

        if session.item != '':
            t_condition = t_condition+" and item_id = '"+str(item_id)+"'"

        if session.transaction_type != '':
            t_condition = t_condition+" and transaction_type = '"+str(transaction_type)+"'"
       
    if all_button == "All":
        t_condition = ""
        session.filter_button = None
        session.item = ""
        session.transaction_type = ""
        session.from_dt = ""
        session.to_dt = ""

    if user_type == 'Admin':
        counter_market_transaction_sql = "SELECT * from counter_market_transaction where cid = '"+c_id+"' "+ t_condition+"  order by id desc limit %d, %d" % limit_by
        counter_market_transaction_rec = db.executesql(counter_market_transaction_sql, as_dict=True)

        get_total_record_sql = "SELECT * from counter_market_transaction where cid = '"+c_id+"' "+ t_condition+"  order by id desc;"
        get_total_record = db.executesql(get_total_record_sql, as_dict=True)

    elif user_type == 'Depot':
        depot_id=session.depot_id
        counter_market_transaction_sql = "SELECT * from counter_market_transaction where cid = '"+c_id+"' "+ t_condition+" and depot_id ='"+str(depot_id)+"'  order by id desc limit %d, %d" % limit_by
        counter_market_transaction_rec = db.executesql(counter_market_transaction_sql, as_dict=True)

        get_total_record_sql = "SELECT * from counter_market_transaction where cid = '"+c_id+"' "+ t_condition+" and depot_id ='"+str(depot_id)+"'  order by id desc ;"
        get_total_record = db.executesql(get_total_record_sql, as_dict=True)


    session.t_condition = t_condition

    
    return dict(counter_market_transaction_rec=counter_market_transaction_rec, page_Number=page_Number, item_per_page = item_per_page, get_total_record =get_total_record)




#======================================= COUNTER MARKET TRANSACTION LIST DOWNLOAD =====================================#

def counter_market_transaction_show_Download():
    c_id = session.cid
    # depot_id = session.depot_id
    t_condition = session.t_condition
    user_type = session.user_type

    if user_type == 'Admin':
        counter_market_transaction_sql = "SELECT * from counter_market_transaction where cid = '"+c_id+"' "+ t_condition+"  order by id desc;"
        counter_market_transaction_data = db.executesql(counter_market_transaction_sql, as_dict=True)

    elif user_type == 'Depot':
        depot_id=session.depot_id
        counter_market_transaction_sql = "SELECT * from counter_market_transaction where cid = '"+c_id+"' "+ t_condition+" and depot_id ='"+str(depot_id)+"'  order by id desc ;"
        counter_market_transaction_data = db.executesql(counter_market_transaction_sql, as_dict=True)

    # return record
    myString = 'Counter Market Transaction List\n\n'
    myString += 'Depot ID, Depot Name, Item ID, Item Name, Transaction Type, Transaction Date, Item Per Unit, Quality, Counter Quality \n'
    total=0
    attTime = ''
    totalCount = 0
    for c in range(len(counter_market_transaction_data)):
        records_ov_dict=counter_market_transaction_data[c]   
        record_id=str(records_ov_dict["id"])
        depot_id=str(records_ov_dict["depot_id"])
        depot_name=str(records_ov_dict["depot_name"])
        item_id=str(records_ov_dict["item_id"])
        item_name=str(records_ov_dict["item_name"])
        transaction_type=str(records_ov_dict["transaction_type"])   
        transaction_date=str(records_ov_dict["transaction_date"])   
        Item_per_unit=str(records_ov_dict["Item_per_unit"])
        qty=str(records_ov_dict["qty"])
        counter_qty=records_ov_dict["counter_qty"]
        
        myString += str(depot_id) + ',' + str(depot_name) + ',' + str(item_id) + ',' + str(item_name) + ',' + str(transaction_type) + ',' + str(transaction_date) + ',' + str(Item_per_unit) + ',' + str(qty) + ',' + str(counter_qty) + '\n'

    # Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=counter_market_transaction_list.csv'
    return str(myString)
