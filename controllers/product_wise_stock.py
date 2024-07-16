# ================================= COUNTER MARKET TRANSACTION SHOW ============================================ #

def product_stock():  
    

    # if ((session.cid==None) or (session.cid=='None')):
    #     redirect(URL('default','index'))
    depot_available_stock = []
    depot_stock_balance = []
    response.title='Counter Item Stock'
    c_id=session.cid
    user_type = session.user_type
    # return session.depot_id
    # depot_id=session.depot_id
    item=str(request.vars.item_id).strip().replace('None','')
    
    depot_ID=str(request.vars.depot_ID).strip().replace('None','')
    
    '''
    print('item', item)
    print('depot_id: ', depot_ID)
    print('session: ', session.user_type)
    print('session: ',session.user_type)
    '''

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

    # ========================= console check =========================
    check_init = dict(user_type = user_type, item_id = item_id, item_name = item_name, depot_id = depot_ID, depot_name = depot_name, filter_button = filter_button, all_button = all_button)
    

#========================= PAGING ==============================
    if len(request.args):
        page_Number = int(request.args[0])
        # return page
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
            item_condition = item_condition+" and sdsb.item_id = '"+str(item_id)+"'"

        if session.depot_ID != '':
            item_condition = item_condition+" and sdsb.depot_id = '"+str(depot_ID)+"'"
        session.item_condition = item_condition
       
    if all_button == "All":
        session.filter_button = None
        session.item = ""
        item_condition = ""
        session.depot_ID = ""
        session.item_condition = ""
        session.filter_button = ""


    # print('item condition: ', item_condition)

    # return session.filter_button
    if session.filter_button == '' or session.filter_button == 'None' or session.filter_button == None or session.filter_button == 'NONE':
        
        if user_type == 'Admin':
            sql_query_depot_available_stock = "select si.item_id, si.name, si.unit_type as size, sum(sdsb.quantity + sdsb.counter_qty / case when si.item_per_unit = 0 then 1 else si.item_per_unit end) as available_stock, si.price from sm_item as si inner join sm_depot_stock_balance as sdsb on sdsb.item_id = si.item_id where sdsb.cid = '"+c_id+"' and sdsb.store_name = 'Commercial' group by sdsb.item_id order by si.name limit %d, %d" % limit_by
    
            depot_available_stock = db.executesql(sql_query_depot_available_stock, as_dict = True)

            get_total_record_sql = "SELECT COUNT(*) AS total_item FROM (select sdsb.item_id from sm_item as si inner join sm_depot_stock_balance as sdsb on sdsb.item_id = si.item_id where sdsb.cid = '"+c_id+"' group by sdsb.item_id) as Total_Items"
            # return get_total_record_sql
            get_total_record = db.executesql(get_total_record_sql, as_dict=True)

        elif user_type == 'Depot':
            depot_id = session.depot_id
            
        
            sql_query_depot_available_stock = "select si.item_id, si.name, si.unit_type as size, sum(sdsb.quantity + sdsb.counter_qty / case when si.item_per_unit = 0 then 1 else si.item_per_unit end) as available_stock, si.price from sm_item as si inner join sm_depot_stock_balance as sdsb on sdsb.item_id = si.item_id where sdsb.depot_id ='"+str(depot_id)+"' and sdsb.cid = '"+c_id+"' group by sdsb.item_id order by si.name limit %d, %d" % limit_by
    
            depot_available_stock = db.executesql(sql_query_depot_available_stock, as_dict = True)

            get_total_record_sql = "SELECT COUNT(*) AS total_item FROM (select sdsb.item_id from sm_item as si inner join sm_depot_stock_balance as sdsb on sdsb.item_id = si.item_id where sdsb.depot_id ='"+str(depot_id)+"' and sdsb.cid = '"+c_id+"' group by sdsb.item_id) as Total_Items"

            # return get_total_record_sql
            get_total_record = db.executesql(get_total_record_sql, as_dict=True)
    else:
    
        if user_type == 'Admin':
           
            sql_query_depot_available_stock = "select si.item_id, si.name, si.unit_type as size, sum(sdsb.quantity + sdsb.counter_qty / case when si.item_per_unit = 0 then 1 else si.item_per_unit end) as available_stock, si.price from sm_item as si inner join sm_depot_stock_balance as sdsb on sdsb.item_id = si.item_id where sdsb.cid = '"+c_id+"' "+session.item_condition+" and sdsb.store_name = 'Commercial' group by sdsb.item_id order by si.name limit %d, %d" % limit_by
    
            depot_available_stock = db.executesql(sql_query_depot_available_stock, as_dict = True)

            get_total_record_sql = "SELECT COUNT(*) AS total_item FROM (select sdsb.item_id from sm_item as si inner join sm_depot_stock_balance as sdsb on sdsb.item_id = si.item_id where sdsb.cid = '"+c_id+"' "+ session.item_condition+" and sdsb.store_name = 'Commercial' group by sdsb.item_id) as Total_Items"

            # return get_total_record_sql
            get_total_record = db.executesql(get_total_record_sql, as_dict=True)

        elif user_type == 'Depot':
            depot_id = session.depot_id
            zero_check = "(case when si.item_per_unit = 0 then 1 else si.item_per_unit end)"
            sql_query_depot_available_stock = "select si.item_id, si.name, si.unit_type as size, sum(sdsb.quantity + sdsb.counter_qty / case when si.item_per_unit = 0 then 1 else si.item_per_unit end) as available_stock, si.price from sm_item as si inner join sm_depot_stock_balance as sdsb on sdsb.item_id = si.item_id where sdsb.depot_id ='"+str(depot_id)+"' and sdsb.cid = '"+c_id+"' "+session.item_condition+" group by sdsb.item_id order by si.name limit %d, %d" % limit_by

            depot_available_stock = db.executesql(sql_query_depot_available_stock, as_dict = True)

            get_total_record_sql = "SELECT COUNT(*) AS total_item FROM (select sdsb.item_id from sm_item as si inner join sm_depot_stock_balance as sdsb on sdsb.item_id = si.item_id where sdsb.depot_id ='"+str(depot_id)+"' and sdsb.cid = '"+c_id+"' "+session.item_condition+" group by sdsb.item_id) as Total_Items"
            get_total_record = db.executesql(get_total_record_sql, as_dict=True)
        
    
    

    # session.item_condition = item_condition
    
    return dict(page_Number=page_Number, item_per_page = item_per_page, get_total_record = get_total_record[0]['total_item'], depot_available_stock = depot_available_stock)




#======================================= COUNTER MARKET TRANSACTION LIST DOWNLOAD =====================================#

def product_stock_Download():
    c_id = session.cid
    item_condition = session.item_condition

    # depot_id = session.depot_id
    user_type = session.user_type
    if item_condition == None:
        item_condition = ''

    if user_type == 'Admin':
        sql_query_depot_available_stock = "select si.item_id, si.name, si.unit_type as size, sum(sdsb.quantity + sdsb.counter_qty / case when si.item_per_unit = 0 then 1 else si.item_per_unit end) as available_stock, si.price from sm_item as si inner join sm_depot_stock_balance as sdsb on sdsb.item_id = si.item_id where sdsb.cid = '"+c_id+"' "+item_condition+" and sdsb.store_name = 'Commercial' group by sdsb.item_id order by sdsb.item_id"

    elif user_type == 'Depot':
        depot_id=session.depot_id
        sql_query_depot_available_stock = "select si.item_id, si.name, si.unit_type as size, sum(sdsb.quantity + sdsb.counter_qty / case when si.item_per_unit = 0 then 1 else si.item_per_unit end) as available_stock, si.price from sm_item as si inner join sm_depot_stock_balance as sdsb on sdsb.item_id = si.item_id where sdsb.depot_id ='"+str(depot_id)+"' and sdsb.cid = '"+c_id+"' "+item_condition+" group by sdsb.item_id order by sdsb.item_id"
    
    depot_available_stock = db.executesql(sql_query_depot_available_stock, as_dict=True)

    # return depot_stock_balance_sql
    myString = 'Product Wise Inventory\n\n'
    myString += 'P Code, Product Of Name, Size, M.R.P, Available Stock \n'
    total=0
    attTime = ''
    totalCount = 0
    for item in range(len(depot_available_stock)):
        records_ov_dict=depot_available_stock[item]   
        product_id=str(records_ov_dict["item_id"])
        name=str(records_ov_dict["name"])
        price=str(records_ov_dict["price"])
        available_stock=str(records_ov_dict["available_stock"])
        size=str(records_ov_dict["size"])                                     

        myString += str(product_id) + ',' + str(name) + ',' + str(size) + ',' + str(price) + ',' + str(available_stock) + '\n'

    # Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=product_wise_stock.csv'
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