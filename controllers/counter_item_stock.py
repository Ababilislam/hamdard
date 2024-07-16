# ================================= COUNTER MARKET TRANSACTION SHOW ============================================ #

def counter_item_stock():  
    if ((session.cid==None) or (session.cid=='None')):
        redirect(URL('default','index'))
    response.title='Counter Item Stock'
    c_id=session.cid
    user_type = session.user_type

    item=str(request.vars.item_id).strip().replace('None','')
    depot_ID=str(request.vars.depot_ID).strip().replace('None','')
    try:
        item_id = str(request.vars.item_id).split('|')[0]
        item_name = str(request.vars.item_id).split('|')[1]
    except:
        item_id = ''
        item_name = ''
    try:
        depot_ID = str(request.vars.depot_ID).split('|')[0]
        depot_name = str(request.vars.depot_ID).split('|')[1]
    except:
        depot_ID = ''
        depot_name = ''
    
    filter_button = str(request.vars.btn_filter).strip()
    all_button = str(request.vars.btn_all).strip()
    item_condition=''
    get_total_record = 0
    get_total_record = 0

#========================= PAGING ==============================
    if len(request.args):
        page_Number = int(request.args[0])
    else:
        page_Number = 0
    item_per_page = 20
    if page_Number is not None and item_per_page is not None:
        # limit_by = ((page_Number + 1) * item_per_page , item_per_page )
        limit_by = (page_Number * item_per_page,  item_per_page + 1)

#========================= PAGING ==============================

    if filter_button == "Filter":
        session.filter_button = filter_button
        session.item = item
        session.depot_ID = depot_ID

        if session.item != '':
            item_condition += f"and dsb.item_id = '{item_id}'"

        if session.depot_ID != '':
            item_condition += f"and depot_id = '{depot_ID}'"
        session.item_condition = item_condition
       
    if all_button == "All":
        session.filter_button = None
        session.item = ""
        item_condition = ""
        session.depot_ID = ""
        session.item_condition = ""
        session.filter_button = ""
    
    limit_start, limit_end = limit_by
    if user_type == 'Admin':
        depot_stock_balance_sql = f""" 
            SELECT dsb.*, i.item_id as I_ITEM_ID, i.name AS item_name, i.item_per_unit 
            FROM sm_depot_stock_balance AS dsb 
            inner JOIN sm_item AS i ON dsb.item_id = i.item_id 
            WHERE dsb.cid = '{c_id}' {item_condition}  AND dsb.store_name = 'Commercial' 
            GROUP BY dsb.item_id,dsb.depot_id
            ORDER BY item_name,dsb.depot_id
            LIMIT %d, %d""" % (limit_start, limit_end)
        depot_stock_balance = db.executesql(depot_stock_balance_sql, as_dict=True)

        get_total_record_sql = f"""SELECT dsb.* from sm_depot_stock_balance  as dsb where cid = '{c_id}' {item_condition} and store_name = 'Commercial' group by depot_id,item_id order by depot_id,item_id """
        get_total_record = db.executesql(get_total_record_sql, as_dict=True)

    elif user_type == 'Depot':
        depot_id = session.depot_id
        depot_stock_balance_sql = f"""
            SELECT dsb.*, i.item_id as I_ITEM_ID, i.name AS item_name, i.item_per_unit 
            FROM sm_depot_stock_balance AS dsb 
            LEFT JOIN sm_item AS i ON dsb.item_id = i.item_id 
            WHERE dsb.cid = '{c_id}' {item_condition} and depot_id = '{depot_id}'  AND dsb.store_name = 'Commercial' 
            GROUP BY dsb.item_id,dsb.depot_id
            ORDER BY item_name,dsb.depot_id
            LIMIT %d, %d
        """ % ( limit_start, limit_end)
        depot_stock_balance = db.executesql(depot_stock_balance_sql, as_dict=True)
        
        get_total_record_sql = f"""SELECT dsb.* from sm_depot_stock_balance as dsb where cid =  '{c_id}' {item_condition} and depot_id = '{depot_id}'  and store_name = 'Commercial' group by depot_id,item_id order by depot_id,item_id """
        get_total_record = db.executesql(get_total_record_sql, as_dict=True)

    get_total_record = len(get_total_record)

    return dict(depot_stock_balance=depot_stock_balance, page_Number=page_Number, item_per_page = item_per_page, get_total_record =get_total_record)



#======================================= COUNTER MARKET TRANSACTION LIST DOWNLOAD =====================================#

def counter_item_stock_Download():
    c_id = session.cid
    item_condition = session.item_condition
    # depot_id = session.depot_id
    user_type = session.user_type
    if item_condition == None:
        item_condition = ''

    if user_type == 'Admin':
        depot_stock_balance_sql = f""" 
        SELECT dsb.*, i.item_id as I_ITEM_ID, i.name AS item_name, i.item_per_unit 
        FROM sm_depot_stock_balance AS dsb 
        inner JOIN sm_item AS i ON dsb.item_id = i.item_id 
        WHERE dsb.cid = '{c_id}' {item_condition}  AND dsb.store_name = 'Commercial' 
        GROUP BY dsb.item_id,dsb.depot_id
        ORDER BY item_name,dsb.depot_id """

    elif user_type == 'Depot':
        depot_id=session.depot_id
        depot_stock_balance_sql = f"""
        SELECT dsb.*, i.item_id as I_ITEM_ID, i.name AS item_name, i.item_per_unit 
        FROM sm_depot_stock_balance AS dsb 
        LEFT JOIN sm_item AS i ON dsb.item_id = i.item_id 
        WHERE dsb.cid = '{c_id}'  {item_condition}  AND dsb.depot_id = '{depot_id}' AND dsb.store_name = 'Commercial' 
        GROUP BY dsb.item_id, dsb.depot_id
        ORDER BY item_name, dsb.depot_id """
        
    sm_depot_stock_balance_rec = db.executesql(depot_stock_balance_sql, as_dict=True)

    myString = 'Depot Stock Inventory\n\n'
    myString += 'Depot ID, Store ID, Store Name, Item ID, Item Name, Batch ID, Expiary Date, Total Stock, Block Quantity, Available Quantity, Counter Quantity \n'
    total=0
    attTime = ''
    totalCount = 0
    available_qty = 0
    for item in range(len(sm_depot_stock_balance_rec)):
        records_ov_dict=sm_depot_stock_balance_rec[item]   
        record_id=str(records_ov_dict["id"])
        depot_id=str(records_ov_dict["depot_id"])
        store_id=str(records_ov_dict["store_id"])
        store_name=str(records_ov_dict["store_name"])
        item_id=str(records_ov_dict["item_id"])                                                                       
        item_name=records_ov_dict["item_name"]
        item_per_unit=records_ov_dict["item_per_unit"]
        batch_id=records_ov_dict["batch_id"]
        expiary_date=records_ov_dict["expiary_date"]
        quantity=(records_ov_dict["quantity"])
        block_qty=str(records_ov_dict["block_qty"])
        available_qty = int(quantity) - int(block_qty)
        counter_qty=records_ov_dict["counter_qty"]

        myString += str(depot_id) + ',' + str(store_id) + ',' + str(store_name) + ',' + str(item_id) + ',' + str(item_name) + ',' + str(batch_id) + ',' + str(expiary_date) + ',' + str(quantity) + ',' + str(block_qty) + ',' + str(available_qty) +','+str(counter_qty)+ '\n'

    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=depot_stock_balance.csv'
    return str(myString)




#=========================== ALL ITEM LIST AUTO COMPLETE FUNCTION  ===============================

def get_all_item_list():
    retStr = ''
    cid = session.cid
    rows = db(db.sm_item.cid == cid).select(db.sm_item.item_id, db.sm_item.name, orderby=db.sm_item.name)
    for row in rows:
        item_id = str(row.item_id)
        name = str(row.name).replace('|', ' ').replace(',', ' ')

        if retStr == '':
            retStr = item_id + '|' + name
        else:
            retStr += ',' + item_id + '|' + name

    return retStr