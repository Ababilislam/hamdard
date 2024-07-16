                   
#===================================== ADD COUNTER MARKET TRANSACTION ================================#

def counter_market_transaction():  
    if ((session.cid==None) or (session.cid=='None')):
        redirect(URL('default','index'))
    response.title='Counter Market Transaction'
    c_id=session.cid
    depot_id = session.depot_id
    depot_name = session.user_depot_name
    transaction_date = str(date_fixed).split(' ')[0]
    save_button =request.vars.save_btn
    update_button =request.vars.update_btn
    submit_all_button =request.vars.submit_all_btn
    cancel_button =request.vars.cancel_btn
    counter_quantity = 0
    quantity_check = 0
    t_sl = 0
    
    depotRecords = "SELECT id,t_sl FROM sm_depot WHERE cid='" + c_id + "' AND depot_id='" + depot_id + "' order by id desc LIMIT 1;"
    depotRecords = db.executesql(depotRecords, as_dict=True)
    for l in range(len(depotRecords)):
        depotRecordsStr = depotRecords[l]
        row_id = str(depotRecordsStr['id'])
        t_sl = int(depotRecordsStr['t_sl']) + 1

    if save_button:
        t_sl = str(request.vars.t_sl_id).replace('None', '')
        search_type =str(request.vars.search_type).strip()
        try:
            item_id =str(request.vars.item_id).strip().split('|')[0]
            item_name =str(request.vars.item_id).strip().split('|')[1]
        except:
            item_id = ''
            item_name = ''

        item_per_unit =request.vars.item_per_unit_id
        quantity =request.vars.quantity_id
        item = str(request.vars.item_id)
        session.search_type = search_type
        session.item = item
        session.item_per_unit = item_per_unit
        session.quantity = quantity

        if item_id!='' and item_per_unit!='' and quantity != '':

            if quantity == 0 or quantity =='0':
                session.flash = 'Quantity should not be 0'
                redirect(URL(c='counter_market_transaction',f='counter_market_transaction'))

            else:
                if session.search_type == 'market_to_counter':
                    check_item_qty_sql = "SELECT quantity from sm_depot_stock_balance where cid = '"+c_id+"' and depot_id ='"+str(depot_id)+"' and item_id ='"+str(item_id)+"' and store_name ='Commercial' LIMIT 1;"
                    check_item_qty = db.executesql(check_item_qty_sql, as_dict=True)
                    for q in range(len(check_item_qty)):
                        records_dict=check_item_qty[q]
                        stock_qty = records_dict["quantity"]

                    if int(quantity) > int(stock_qty):
                        session.flash = 'Quantity should be lees than Stock quantity'
                        redirect(URL(c='counter_market_transaction',f='counter_market_transaction'))
                    else:
                        check_exits_item_sql = "SELECT * FROM counter_market_transaction_temp where cid = '"+c_id+"' and depot_id ='"+str(depot_id)+"' and item_id ='"+str(item_id)+"' and transaction_type = '"+str(session.search_type)+"'"
                        check_exits_item = db.executesql(check_exits_item_sql, as_dict=True)

                        if len(check_exits_item) == 0:
                            counter_quantity = int(item_per_unit) * int(quantity)
                            insert_market_to_counter_sql = "INSERT INTO counter_market_transaction_temp (cid, t_sl, depot_id, depot_name, item_id, item_name, transaction_type, Item_per_unit, qty, counter_qty, transaction_date) VALUES ('"+str(c_id)+"', '"+str(t_sl)+"', '"+str(depot_id)+"', '"+str(depot_name)+"','"+str(item_id)+"','"+str(item_name)+"','"+str(search_type)+"','"+str(item_per_unit)+"', '"+str(quantity)+"', '"+str(counter_quantity)+"', '"+str(transaction_date)+"')"
                            insert_market_to_counter = db.executesql(insert_market_to_counter_sql)

                            session.search_type = ''
                            session.item = ''
                            session.item_per_unit = ''
                            session.quantity = ''
                            session.flash= 'Insert Successfully'
                            redirect (URL('counter_market_transaction','counter_market_transaction'))
                        else:
                            session.flash= 'This Item Already Exits'
                            redirect (URL('counter_market_transaction','counter_market_transaction'))

                elif session.search_type == 'counter_to_market':
                    check_item_qty_sql = "SELECT counter_qty from sm_depot_stock_balance where cid = '"+c_id+"' and depot_id ='"+str(depot_id)+"' and item_id ='"+str(item_id)+"' and store_name ='Commercial' LIMIT 1;"
                    check_item_qty = db.executesql(check_item_qty_sql, as_dict=True)
                    for q in range(len(check_item_qty)):
                        records_dict=check_item_qty[q]
                        stock_qty = records_dict["counter_qty"]

                    if int(quantity) > int(stock_qty):
                        session.flash = 'Quantity should be lees than Stock quantity'
                        redirect(URL(c='counter_market_transaction',f='counter_market_transaction'))

                    else:
                        check_exits_item_sql = "SELECT * FROM counter_market_transaction_temp where cid = '"+c_id+"' and depot_id ='"+str(depot_id)+"' and item_id ='"+str(item_id)+"' and transaction_type = '"+str(session.search_type)+"'"
                        check_exits_item = db.executesql(check_exits_item_sql, as_dict=True)
                        if len(check_exits_item) == 0:
                            quantity_check = int(quantity) % int(item_per_unit)
                            if quantity_check != 0:
                                session.flash = 'Plase Insert valid Quantity'
                                redirect (URL('counter_market_transaction','counter_market_transaction'))

                            else:
                                qty = int(quantity) / int(item_per_unit)  
                                insert_counter_to_market_sql = "INSERT INTO counter_market_transaction_temp (cid, t_sl, depot_id, depot_name, item_id, item_name, transaction_type, Item_per_unit, qty, counter_qty, transaction_date) VALUES ('"+str(c_id)+"', '"+str(t_sl)+"',  '"+str(depot_id)+"', '"+str(depot_name)+"','"+str(item_id)+"','"+str(item_name)+"','"+str(search_type)+"','"+item_per_unit+"', '"+str(quantity)+"', '"+str(quantity)+"', '"+str(transaction_date)+"')"      
                                insert_counter_to_market = db.executesql(insert_counter_to_market_sql)

                                session.search_type = ''
                                session.item = ''
                                session.item_per_unit = ''
                                session.quantity = ''
                                session.flash= 'Insert Successfully'
                                redirect (URL('counter_market_transaction','counter_market_transaction'))
                        else:
                            session.flash= 'This Item Already Exits'
                            redirect (URL('counter_market_transaction','counter_market_transaction'))

        else:
            session.flash = 'Plase Insert Require Field'
            session.search_type = ''
            redirect (URL('counter_market_transaction','counter_market_transaction'))

    if update_button: 
        record_id = request.args(0)
        item_id = request.args(1)
        item_per_unit = request.args(2)
        qty = request.args(3)
        transaction_type = request.args(4)
        stock_qty = 0
        total_update_price = 0
        update_qty = request.vars.quantity_id
        
        if update_qty == 0 or update_qty =='0':
            session.flash = 'Quantity should not be 0'
            redirect(URL(c='counter_market_transaction',f='counter_market_transaction'))
       
        else:
            if transaction_type == 'market_to_counter':
                check_item_qty_sql = "SELECT quantity from sm_depot_stock_balance where cid = '"+c_id+"' and depot_id ='"+str(depot_id)+"' and item_id ='"+str(item_id)+"' and store_name ='Commercial' LIMIT 1;"
                check_item_qty = db.executesql(check_item_qty_sql, as_dict=True)
                for q in range(len(check_item_qty)):
                    records_dict=check_item_qty[q]
                    stock_qty = records_dict["quantity"]

                if int(update_qty) > int(stock_qty):
                    session.flash = 'Quantity should be lees than Stock quantity'
                    redirect(URL(c='counter_market_transaction',f='counter_market_transaction'))

                else:
                    counter_quantity = int(update_qty) * int(item_per_unit)
                    counter_quantity = int(counter_quantity)

                    update_qty_sql= " Update counter_market_transaction_temp Set qty ='"+str(update_qty)+"', counter_qty ='"+str(counter_quantity)+"' WHERE cid = '"+c_id+"' and depot_id ='"+str(depot_id)+"' and id = '"+str(record_id)+"' LIMIT 1;"  
                    update_qty_record = db.executesql(update_qty_sql)

            elif transaction_type == 'counter_to_market':
                check_item_qty_sql = "SELECT counter_qty from sm_depot_stock_balance where cid = '"+c_id+"' and depot_id ='"+str(depot_id)+"' and item_id ='"+str(item_id)+"' and store_name ='Commercial' LIMIT 1;"
                check_item_qty = db.executesql(check_item_qty_sql, as_dict=True)
                for q in range(len(check_item_qty)):
                    records_dict=check_item_qty[q]
                    stock_qty = records_dict["counter_qty"]

                if int(update_qty) > int(stock_qty):
                    session.flash = 'Quantity should be lees than Stock quantity'
                    redirect(URL(c='counter_market_transaction',f='counter_market_transaction'))

                else:
                    quantity_check = int(update_qty) % int(item_per_unit)
                    if quantity_check != 0:
                        session.flash = 'Plase Insert valid Quantity'
                        redirect (URL('counter_market_transaction','counter_market_transaction'))

                    else:
                        update_qty_sql= " Update counter_market_transaction_temp Set qty ='"+str(update_qty)+"', counter_qty ='"+str(update_qty)+"' WHERE cid = '"+c_id+"' and depot_id ='"+str(depot_id)+"' and id = '"+str(record_id)+"' LIMIT 1;"  
                        update_qty_record = db.executesql(update_qty_sql)

            session.flash = 'Quantity updated Successfully'
            redirect(URL(c='counter_market_transaction',f='counter_market_transaction'))

    if submit_all_button:
        t_sl = request.args(0)
        counter_market_transaction_temp_sql = "SELECT * FROM counter_market_transaction_temp where cid = '"+c_id+"' and depot_id ='"+str(depot_id)+"' and t_sl = '"+t_sl+"';"
        counter_market_transaction_temp_data = db.executesql(counter_market_transaction_temp_sql, as_dict=True)
        for counter in range(len(counter_market_transaction_temp_data)):
            counter_records=counter_market_transaction_temp_data[counter]  
            record_id=str(counter_records["id"])
            t_sl=str(counter_records["t_sl"])
            depot_id=str(counter_records["depot_id"])
            depot_name=str(counter_records["depot_name"])
            item_id=str(counter_records["item_id"])
            item_name=str(counter_records["item_name"])
            transaction_type= counter_records["transaction_type"]
            Item_per_unit= counter_records["Item_per_unit"]
            qty= counter_records["qty"]
            counter_qty=counter_records["counter_qty"]
            transaction_date=counter_records["transaction_date"]

            insert_counter_market_sql = "INSERT INTO counter_market_transaction (cid, t_sl, depot_id, depot_name, item_id, item_name, transaction_type, Item_per_unit, qty, counter_qty, transaction_date) VALUES ('"+str(c_id)+"', '"+str(t_sl)+"',  '"+str(depot_id)+"', '"+str(depot_name)+"','"+str(item_id)+"','"+str(item_name)+"','"+str(transaction_type)+"','"+str(Item_per_unit)+"', '"+str(qty)+"', '"+str(counter_qty)+"', '"+str(transaction_date)+"')"      
            insert_counter_market = db.executesql(insert_counter_market_sql)

            if transaction_type == 'market_to_counter':
                counter_quantity = int(qty) * int(Item_per_unit)
                counter_quantity = int(counter_quantity)

                update_market_to_counter_sql = "UPDATE sm_depot_stock_balance SET quantity = quantity - '" + str(qty) + "', counter_qty = counter_qty + '" + str(counter_quantity) + "' WHERE cid = '" + c_id + "' AND depot_id = '" + str(depot_id) + "' AND item_id = '" + str(item_id) + "' and store_name ='Commercial' LIMIT 1"
                update_market_to_counter = db.executesql(update_market_to_counter_sql)

            elif transaction_type == 'counter_to_market':
                c_quantity = int(qty) / int(Item_per_unit) 

                update_counter_to_market_sql = " UPDATE sm_depot_stock_balance Set quantity = quantity + '" + str(c_quantity) + "', counter_qty = counter_qty - '" + str(qty) + "' where cid = '"+c_id+"' and  depot_id ='"+str(depot_id)+"' and item_id = '"+str(item_id)+"' and store_name ='Commercial' LIMIT 1 "  
                update_counter_to_market = db.executesql(update_counter_to_market_sql)

        delete_sql = "DELETE from counter_market_transaction_temp where cid = '"+c_id+"' and depot_id ='"+str(depot_id)+"' and  t_sl = '"+t_sl+"';"
        records_delete = db.executesql(delete_sql) 

        updateDepotRecord = "UPDATE sm_depot SET t_sl='" + str(t_sl) + "' WHERE id='" + row_id + "' and depot_id ='"+str(depot_id)+"';"
        updateDepotRecord = db.executesql(updateDepotRecord)

        session.flash = 'Transaction Successfull'
        redirect (URL('counter_market_transaction','counter_market_transaction'))

    if cancel_button == 'Cancel':
        t_sl = request.args(0) 
        delete_counter_market_transaction_temp_sql = "DELETE from counter_market_transaction_temp where cid = '"+c_id+"' and depot_id ='"+str(depot_id)+"' and t_sl = '"+t_sl+"';"
        delete_counter_market_transaction_temp = db.executesql(delete_counter_market_transaction_temp_sql)

        updateDepotRecord = "UPDATE sm_depot SET t_sl='" + str(t_sl) + "' WHERE id='" + row_id + "' and depot_id ='"+str(depot_id)+"';"
        updateDepotRecord = db.executesql(updateDepotRecord)

        session.search_type = ''
        session.item = ''
        session.item_per_unit = ''
        session.quantity = ''

        session.flash = 'Canceled Successfully'
        redirect (URL('counter_market_transaction','counter_market_transaction'))

    counter_market_transaction_temp_record_sql = "SELECT * FROM counter_market_transaction_temp where cid = '"+c_id+"' and depot_id ='"+str(depot_id)+"' order by id desc;"
    counter_market_transaction_temp_record = db.executesql(counter_market_transaction_temp_record_sql, as_dict=True)
  
    return dict(counter_market_transaction_temp_record = counter_market_transaction_temp_record, t_sl=t_sl)




#==================================== COUNTER MARKET TRANSACTION DELETE INDIVIDUAL ITEM FUNCTION  ===================================

def counter_market_transaction_delete():
    c_id=session.cid
    depot_id = session.depot_id
    response.title='Counter Market Transaction Delete'
    record_id = request.args(0)

    delete_sql = "DELETE from counter_market_transaction_temp where cid = '"+c_id+"' and depot_id ='"+str(depot_id)+"' and id = '"+record_id+"' LIMIT 1;"
    # return delete_sql
    records = db.executesql(delete_sql)

    session.flash = 'Deleted Successfully'
    redirect (URL('counter_market_transaction','counter_market_transaction'))



#=========================== ACTIVE ITEM LIST AUTO COMPLETE FUNCTION  ===============================

def get_active_item_list():
    retStr = ''
    cid = session.cid
    rows = db((db.sm_item.cid == cid) & (db.sm_item.status == 'ACTIVE')).select(db.sm_item.item_id, db.sm_item.name, orderby=db.sm_item.name)
    for row in rows:
        item_id = str(row.item_id)
        name = str(row.name).replace('|', ' ').replace(',', ' ')

        if retStr == '':
            retStr = item_id + '|' + name
        else:
            retStr += ',' + item_id + '|' + name

    return retStr



#=========================== ITEM PER UNIT AUTO COMPLETE FUNCTION  ===============================
         
def get_item_per_unit():
    c_id = session.cid
    depot_id = session.depot_id
    recStr = ''
    item_id=request.vars.item_id
    itemRows_sql = "select item_per_unit from sm_item where cid = '"+c_id+"' and item_id = '"+str(item_id)+"' order by item_id;"
    itemRows = db.executesql(itemRows_sql, as_dict=True)
    for i in range(len(itemRows)):
        records_ov_dict=itemRows[i]   
        item_per_unit=str(records_ov_dict["item_per_unit"])
        # physician_name=str(records_ov_dict["physician_name"])
        if recStr == '':
            recStr = item_per_unit
        else:
            recStr += ',' +item_per_unit
    
    return recStr



#=========================== COUNTER MARKET TRANSACTION DOWNLOAD FUNCTION  ===============================

def counter_market_transaction_Download():
    cid = session.cid
    depot_id = session.depot_id

    # counter_market_transaction_sql = "SELECT counter_market_transaction.id, counter_market_transaction.depot_id, counter_market_transaction.depot_name, counter_market_transaction.item_id, counter_market_transaction.item_name, counter_market_transaction.transaction_type, counter_market_transaction.Item_per_unit, counter_market_transaction.qty, counter_market_transaction.counter_qty, sm_depot_stock_balance.quantity, sm_depot_stock_balance.counter_qty as depot_counter_qty FROM counter_market_transaction INNER JOIN sm_depot_stock_balance ON counter_market_transaction.item_id = sm_depot_stock_balance.item_id  where counter_market_transaction.cid = '"+str(cid)+"' AND counter_market_transaction.depot_id = '"+str(depot_id)+"' AND sm_depot_stock_balance.depot_id =  '"+str(depot_id)+"'  order by counter_market_transaction.id desc limit 1"
    counter_market_transaction_sql = "SELECT id, depot_id, depot_name, item_id, item_name, transaction_type, Item_per_unit, qty, counter_qty  FROM counter_market_transaction  where cid = '"+str(cid)+"' AND depot_id = '"+str(depot_id)+"' order by id desc limit 100"
    # return counter_market_transaction_sql
    records = db.executesql(counter_market_transaction_sql, as_dict=True)

    myString = 'Counter Market Transaction List\n\n'
    myString += ' Depot ID, Depot Name , Item ID , Item Neme , Transaction Type, Item Per Unit, Quantity, Counter QTY, Transaction Date \n'
    total=0
    attTime = ''
    totalCount = 0

    for i in range(len(records)):
        recordsStr = records[i]
        depot_id = str(recordsStr['depot_id'])
        depot_name = str(recordsStr['depot_name'])
        item_id = str(recordsStr['item_id'])
        item_name = str(recordsStr['item_name'])
        transaction_type = str(recordsStr['transaction_type'])
        Item_per_unit = str(recordsStr['Item_per_unit'])
        qty = str(recordsStr['qty'])
        counter_qty = str(recordsStr['counter_qty'])         
        transaction_date = str(recordsStr['transaction_date'])         
        
        myString += str(depot_id) + ','+str(depot_name) + ',' + str(item_id) + ',' +str(item_name) + ',' + str(transaction_type) + ',' + str(Item_per_unit) + ',' + str(qty) + ',' + str(counter_qty)+ ' ,' + str(transaction_date)+ ' \n'

    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=Counter_Market_Transaction_List.csv'
    
    return str(myString)



#=========================== SM DEPOT STOCK BALANCE DOWNLOAD FUNCTION  ===============================


def stock_download():
    cid = session.cid
    depot_id = session.depot_id

    sm_depot_stock_balance_sql = "SELECT * FROM sm_depot_stock_balance  where cid = '"+str(cid)+"' AND depot_id = '"+str(depot_id)+"' and store_name ='Commercial' group by item_id "
    depot_stock_balance = db.executesql(sm_depot_stock_balance_sql, as_dict=True)

    myString_str = 'Depot Stock Balance List List\n\n'
    myString_str += ' Depot ID, Store ID, Store Name, Item ID , Batch ID, Expiry Date, Quantity, Counter QTY \n'
    total = 0
    attTime = ''
    totalCount = 0

    for i in range(len(depot_stock_balance)):
        recordsStr_stock = depot_stock_balance[i]
        depot_id = str(recordsStr_stock['depot_id'])
        store_id = str(recordsStr_stock['store_id'])
        store_name = str(recordsStr_stock['store_name'])
        item_id = str(recordsStr_stock['item_id'])
        batch_id = str(recordsStr_stock['batch_id'])
        expiary_date = str(recordsStr_stock['expiary_date'])
        quantity = str(recordsStr_stock['quantity'])
        counter_qty = str(recordsStr_stock['counter_qty'])
        
        myString_str += str(depot_id) + ',' + str(store_id) + ',' + str(store_name) + ',' + str(item_id) + ',' + str(batch_id) + ',' + str(expiary_date) + ',' + str(quantity) + ',' + str(counter_qty) + ',\n'

    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=Sm_Depot_Stock_Balance_List.csv'
    return str(myString_str)  

