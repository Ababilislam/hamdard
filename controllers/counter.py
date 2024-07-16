                   
#==================================== COUNTER INVOICE MEMO ADD ITEM ====================================

def counter_add():  

    response.title='Counter Memo'
    c_id=session.cid
    depot_id = session.depot_id
    depot_name = session.user_depot_name
    save_button =request.vars.submit_btn
    cancel_btn =request.vars.cancel_btn
    update_btn =request.vars.update_btn
    submit_all_button =request.vars.submit_all_btn
    import_button =request.vars.import_btn
    invoice_counter_record = ''

    from datetime import datetime
    current_datetime = date_fixed
    year = current_datetime.year
    month = current_datetime.month
    first_date_of_month = datetime(year, month, 1)
    first_date_str = first_date_of_month.strftime("%Y-%m-%d")

    current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    status = 'Invoiced'
    temp_status = 'Submitted'
    order_sl = 0
    item_per_unit = 1
    total_depot_stock_qty = 0
    depot_row_id = 0

    depotRecords = "SELECT id,order_sl_counter FROM sm_depot WHERE cid='" + c_id + "' AND depot_id='" + depot_id + "' order by id desc LIMIT 1;"
    depotRecords = db.executesql(depotRecords, as_dict=True)

    for l in range(len(depotRecords)):
        depotRecordsStr = depotRecords[l]
        depot_row_id = str(depotRecordsStr['id'])
        order_sl = int(depotRecordsStr['order_sl_counter']) + 1

    #================================ SAVE BUTTON CLICK =================================#

    if save_button == 'Save':
        order_sl = str(request.vars.order_sl_id).replace('None', '')
        sales_date = request.vars.sales_date_id

        try:
            physician_id =str(request.vars.physician_id).strip().split('|')[0]
            physician_name =str(request.vars.physician_id).strip().split('|')[1]
        except:
            physician_id = 'Counter'
            physician_name = 'Counter'

        discount_type = str(request.vars.discount_type_id).strip().upper().replace('None', '')
        customer_id = str(request.vars.customer_id).strip().replace('None', '')
        phone = str(request.vars.phone).strip()
        customer_name = str(request.vars.customer_name).strip().replace('None', '')
        gender = str(request.vars.gender).strip().replace('None', '')
        age = str(request.vars.age).strip().replace('None', '')
        staff_id = str(request.vars.staff_id).strip().replace('None', '')
        note = str(request.vars.note_id).strip().replace('None', '')
        item_id_check = str(request.vars.item_id)
        item_per_unit = str(request.vars.item_per_unit)
        quantity =request.vars.qty_id
        counter_stock_qty =request.vars.stock_qty
        depot_stock_qty =request.vars.depot_stock_qty
        total_depot_stock_qty = (int(depot_stock_qty) * int(item_per_unit)) + int(counter_stock_qty)
        customer_category = ''

        try:
            item_id =str(request.vars.item_id).strip().split('|')[0]
            item_name =str(request.vars.item_id).strip().split('|')[1]
        except:
            item_id = ''
            item_name = ''

        physician = str(request.vars.physician_id).replace('None', '')
        session.sales_date = sales_date
        session.physician_id = physician
        session.discount_type = discount_type
        session.customer_id = customer_id
        session.phone = phone
        session.customer_name = customer_name
        session.gender = gender
        session.age = age
        session.staff_id = staff_id
        session.note = note

        if discount_type == 'STAFF':
            customer_category = 'STAFF'
            if staff_id == '' or staff_id == 'None' or staff_id == None:
                session.flash = 'Please Insert Staff ID'
                redirect(URL(c='counter',f='counter_add'))
        else:
            customer_category = 'General Customer'

        if item_id_check =='' or quantity == '' :
            session.flash = 'Please insert require field'
            redirect(URL(c='counter',f='counter_add'))

        if quantity == '0' or quantity == 0:
            session.flash = 'Quantity should not be 0'
            redirect(URL(c='counter',f='counter_add'))

        else:
            if int(quantity) > int(counter_stock_qty):
                if int(quantity) > int(total_depot_stock_qty):
                    session.flash = 'Depot Stock Not Available'
                    redirect(URL(c='counter',f='counter_add'))

                # need_import_unit=(int(quantity)-int(counter_stock_qty))/int(item_per_unit)
                # # compare with depot stock qty
                # check_depot_stock_sql = "SELECT quantity FROM sm_depot_stock_balance where cid = '"+c_id+"' and store_name='Commercial' and depot_id='"+str(depot_id)+"' and item_id ='"+str(item_id)+"' group by item_id limit 1 ;"
                # check_depot_stock = db.executesql(check_depot_stock_sql, as_dict=True)
                # for depot_stock_item_n in range(len(check_depot_stock)):
                #     depot_stock_item_dict=check_depot_stock[depot_stock_item_n]
                #     item_depot_stock_n = depot_stock_item_dict["quantity"]
                
                # if int(need_import_unit) <= int(item_depot_stock_n):
                #     pass
                # else:
                #     session.flash = 'Depot stock not Available'
                #     redirect(URL(c='counter',f='counter_add'))

                # counter_quantity = int(item_per_unit) * int(need_import_unit)

                # # return need_import_unit
                # # return counter_quantity
                # update_market_to_counter_sql = "UPDATE sm_depot_stock_balance SET quantity = quantity - '" + str(need_import_unit) + "', counter_qty = counter_qty + '" + str(counter_quantity) + "' WHERE cid = '" + c_id + "' AND depot_id = '" + str(depot_id) + "' AND item_id = '" + str(item_id) + "' and store_name ='Commercial' LIMIT 1"
                # update_market_to_counter = db.executesql(update_market_to_counter_sql)
                # session.flash = 'Quantity Imported Successfully'

                # t_slRecords_sql = "SELECT id,t_sl FROM counter_market_transaction WHERE cid='" + c_id + "' AND depot_id='" + depot_id + "' order by id desc LIMIT 1;"
                # t_slRecords = db.executesql(t_slRecords_sql, as_dict=True)
                # for l in range(len(t_slRecords)):
                #     depotRecords_v = t_slRecords[l]
                #     row_id = str(depotRecords_v['id'])
                #     t_sl = depotRecords_v['t_sl']
                #     t_sl_v=t_sl+1

                # search_type = 'Depot_to_counter'
                # insert_counter_to_market_sql = "INSERT INTO counter_market_transaction(cid, t_sl, depot_id, depot_name, item_id, item_name, transaction_type, Item_per_unit, qty, counter_qty, transaction_date) VALUES ('"+str(c_id)+"', '"+str(t_sl_v)+"', '"+str(depot_id)+"', '"+str(depot_name)+"','"+str(item_id)+"','"+str(item_name)+"','"+str(search_type)+"','"+str(item_per_unit)+"', '"+str(quantity)+"', '"+str(counter_quantity)+"', '"+str(current_datetime)+"')"
                # insert_counter_to_market = db.executesql(insert_counter_to_market_sql)

            price = 0
            discount_percentage = 0.0
            total_price = 0

            select_item_price_sql = "SELECT price,item_per_unit from sm_item where cid = '"+c_id+"' and item_id = '"+str(item_id)+"' group by item_id;"
            select_item_price = db.executesql(select_item_price_sql, as_dict=True)
            for a in range(len(select_item_price)):
                item_record = select_item_price[a]
                price = float(item_record['price'])/int(item_record['item_per_unit'])

            select_discount_percentage_sql = "SELECT discount_percentage from sm_counter_item_discount where cid = '"+c_id+"' AND item_id = '"+str(item_id)+"' AND discount_type = '"+str(discount_type)+"' group by discount_type;"
            select_discount_percentage = db.executesql(select_discount_percentage_sql, as_dict=True)
            for a in range(len(select_discount_percentage)):
                discount_type_record = select_discount_percentage[a]
                discount_percentage = discount_type_record['discount_percentage']

            check_counter_customer_sql = "SELECT * from counter_customer where cid = '"+c_id+"'   and phone = '"+phone+"' group by depot_id,phone "
            check_counter_customer_record = db.executesql(check_counter_customer_sql, as_dict = True)
            if len(check_counter_customer_record) == 0 :
                customer_id_sql = "SELECT id,customer_id FROM counter_customer WHERE cid='" + c_id + "' order by id desc LIMIT 1;"
                customer_Records = db.executesql(customer_id_sql, as_dict=True)

                for c in range(len(customer_Records)):
                    customerRecordsStr = customer_Records[c]
                    rec_id = str(customerRecordsStr['id'])
                    customer_id = int(customerRecordsStr['customer_id']) + 1
 
                phone = int('88'+phone)
                session.customer_id = customer_id

            check_exits_sl_sql = "SELECT order_sl_counter from sm_order_head_counter_temp where cid = '"+c_id+"'  AND depot_id ='"+str(depot_id)+"' AND order_sl_counter = '"+str(order_sl)+"' group by order_sl_counter"
            check_exits_sl = db.executesql(check_exits_sl_sql, as_dict=True)

            if len(check_exits_sl) == 0:
                invoice_counter_head_temp_insert_sql = "INSERT INTO sm_order_head_counter_temp (cid, depot_id, depot_name, order_sl_counter, order_date, order_datetime, physician_id, physician_name, discount_type, note, customer_id, phone, customer_name, gender, age, customer_category, staff_id ) VALUES ('"+str(c_id)+"','"+str(depot_id)+"','"+str(depot_name)+"','"+order_sl+"','"+str(sales_date)+"', '"+str(current_datetime)+"','"+str(physician_id)+"','"+str(physician_name)+"','"+str(discount_type)+"','"+str(note)+"','"+str(customer_id)+"','"+str(phone)+"','"+str(customer_name)+"','"+str(gender)+"','"+str(age)+"','"+str(customer_category)+"','"+str(staff_id)+"');" 
                invoice_counter_head_temp_insert = db.executesql(invoice_counter_head_temp_insert_sql)

            check_same_item_check__sql = "SELECT item_id, item_name, quantity from sm_order_counter_temp where cid = '"+c_id+"'  AND depot_id ='"+str(depot_id)+"' AND order_sl_counter = '"+str(order_sl)+"' AND item_id = '"+str(item_id)+"' AND item_name = '"+str(item_name)+"' group by item_id"
            check_same_item_check = db.executesql(check_same_item_check__sql, as_dict=True)

            if len(check_same_item_check) > 0:
                session.flash = 'Please Select Different Item.'
                redirect(URL(c='counter',f='counter_add'))
            else:
                total_price = int(quantity) * float(price)
                total_price = float(total_price)
                
                invoice_counter_details_insert_sql = "INSERT INTO sm_order_counter_temp (cid, depot_id, depot_name, order_sl_counter, order_date, order_datetime, delivery_date, collection_date, physician_id, physician_name, status, ym_date, discount_type, item_id, item_name, quantity, price, item_discount, total_price ) VALUES ('" + str(c_id) + "','" + str(depot_id) + "','" + str(depot_name) + "','" + order_sl + "','" + str(sales_date) + "', '"+str(current_datetime)+"', '" + str(sales_date) + "', '"+str(sales_date)+"','" + str(physician_id) + "','" + str(physician_name) + "', '" + str(temp_status) + "', '"+str(first_date_str)+"','" + str(discount_type) + "','" + str(item_id) + "','" + str(item_name) + "'," + str(quantity) + "," + str(price) + "," + str(discount_percentage) + "," + str(total_price) + ");"
                invoice_counter_details_insert = db.executesql(invoice_counter_details_insert_sql)
                session.flash = 'Item Insert Successfully'
                redirect(URL(c='counter',f='counter_add'))


    #================================ UPDATE BUTTON CLICK =================================#
    
    if update_btn:
        record_id = request.args(0)
        actual_price = request.args(1)
        item_id = request.args(2)
        counter_stock_qty = 0
        total_update_price = 0
        update_qty = request.vars.quantity_id
        depot_stock_qty = 0

        check_item_qty_sql = "SELECT quantity, counter_qty from sm_depot_stock_balance where cid = '"+c_id+"' and depot_id ='"+str(depot_id)+"' and item_id ='"+str(item_id)+"' and store_name ='Commercial' LIMIT 1;"
        check_item_qty = db.executesql(check_item_qty_sql, as_dict=True)
        for qty in range(len(check_item_qty)):
            records_dict=check_item_qty[qty]
            depot_stock_qty = records_dict["quantity"]
            counter_stock_qty = records_dict["counter_qty"]

        if update_qty == 0 or update_qty =='0':
            session.flash = 'Quantity should not be 0'
            redirect(URL(c='counter',f='counter_add'))

        if int(update_qty) > int(counter_stock_qty):
            if int(update_qty) > int(depot_stock_qty):
                session.flash = 'Quantity Should Be Lees Than Stock quantity'
                redirect(URL(c='counter',f='counter_add'))
            else:
                pass
 
        total_update_price = float(actual_price) * int(update_qty)
        total_update_price = float(total_update_price)
        update_qty_sql= " Update sm_order_counter_temp Set quantity ='"+str(update_qty)+"', total_price ='"+str(total_update_price)+"' WHERE cid = '"+c_id+"' and id = '"+str(record_id)+"' LIMIT 1;"  
        update_qty = db.executesql(update_qty_sql)
        session.flash = 'Quantity updated Successfully'
        redirect(URL(c='counter',f='counter_add'))

    #================================ SUBMIT BUTTON CLICK =================================#

    if submit_all_button == 'Submit':
        get_order_sl = request.args(0)
        grand_price = request.args(1)
        total_discount = request.args(2)
        net_total = request.args(3)
        t_sl = 0
        t_sl_v = 0
        depot_qty_insert = 0

        select_sm_order_head_counter_temp_record_sql = "SELECT * FROM sm_order_head_counter_temp where cid = '"+c_id+"'  AND depot_id ='"+str(depot_id)+"' and order_sl_counter = '"+get_order_sl+"' group by sl limit 1"
        select_sm_order_head_counter_temp_record = db.executesql(select_sm_order_head_counter_temp_record_sql, as_dict=True)

        for item in range(len(select_sm_order_head_counter_temp_record)):
            item_record = select_sm_order_head_counter_temp_record[item]
            depot_id = str(item_record['depot_id'])
            depot_name = str(item_record['depot_name'])
            physician_id = str(item_record['physician_id'])
            physician_name = str(item_record['physician_name'])
            discount_type = str(item_record['discount_type'])
            order_sl_counter = str(item_record['order_sl_counter'])
            order_date = str(item_record['order_date'])
            order_datetime = str(item_record['order_datetime'])
            note = str(item_record['note'])
            customer_id = str(item_record['customer_id'])
            phone = str(item_record['phone'])
            customer_name = str(item_record['customer_name']).replace(',', ' ')
            gender = str(item_record['gender'])
            age = str(item_record['age'])
            customer_category = str(item_record['customer_category'])
            staff_id = str(item_record['staff_id'])

            check_counter_customer_sql = "SELECT * from counter_customer where cid = '"+c_id+"'   and phone = '"+phone+"' group by depot_id,phone "
            check_counter_customer_record = db.executesql(check_counter_customer_sql, as_dict = True)
            if len(check_counter_customer_record) == 0 :
                insert_counter_customer_sql = "INSERT INTO counter_customer(cid, depot_id, depot_name, customer_id, phone, customer_name, gender, age, customer_category, staff_id ) VALUES ('"+str(c_id)+"','"+str(depot_id)+"','"+str(depot_name)+"','"+str(customer_id)+"','"+str(phone)+"','"+str(customer_name)+"','"+str(gender)+"','"+str(age)+"','"+str(customer_category)+"','"+str(staff_id)+"')"
                insert_counter_customer = db.executesql(insert_counter_customer_sql)
            
            check_exits_order_sl_counter_sql = "SELECT order_sl_counter from sm_order_head_counter where cid = '"+c_id+"'  AND depot_id ='"+str(depot_id)+"' AND order_sl_counter = '"+str(order_sl_counter)+"' group by order_sl_counter"
            check_exits_order_sl_counter = db.executesql(check_exits_order_sl_counter_sql, as_dict=True)
            if len(check_exits_order_sl_counter) == 0:
                insert_sm_order_head_counter_sql = "INSERT INTO sm_order_head_counter (cid, depot_id, depot_name, order_sl_counter, order_date, order_datetime, ym_date, status, physician_id, physician_name, discount_type, note, customer_id, phone, customer_name, gender, age, customer_category, staff_id ) VALUES ('"+str(c_id)+"','"+str(depot_id)+"','"+str(depot_name)+"','"+order_sl_counter+"','"+str(order_date)+"', '"+str(current_datetime)+"', '"+str(first_date_str)+"', '"+str(status)+"','"+str(physician_id)+"','"+str(physician_name)+"','"+str(discount_type)+"','"+str(note)+"','"+str(customer_id)+"','"+str(phone)+"','"+str(customer_name)+"','"+str(gender)+"','"+str(age)+"','"+str(customer_category)+"','"+str(staff_id)+"');" 
                insert_sm_order_head_counter = db.executesql(insert_sm_order_head_counter_sql)

            check_exits_order_sl_counter_sql = "SELECT order_sl_counter from sm_invoice_head_counter where cid = '"+c_id+"'  AND depot_id ='"+str(depot_id)+"' AND order_sl_counter = '"+str(order_sl_counter)+"' group by order_sl_counter"
            check_exits_order_sl_counter = db.executesql(check_exits_order_sl_counter_sql, as_dict=True)
            if len(check_exits_order_sl_counter) == 0:
                insert_sm_invoice_head_counter_sql = "INSERT INTO sm_invoice_head_counter (cid, depot_id, depot_name, order_sl_counter, order_date, order_datetime, delivery_date, physician_id, physician_name, discount_type, status, actual_total_tp, discount, total_amount, invoice_date, ym_date, invoice_ym_date, note, customer_id, phone, customer_name, gender, age, customer_category, staff_id) VALUES ('"+str(c_id)+"','"+str(depot_id)+"','"+str(depot_name)+"','"+order_sl_counter+"','"+str(order_date)+"', '"+str(current_datetime)+"', '"+str(order_date)+"', '"+str(physician_id)+"','"+str(physician_name)+"','"+str(discount_type)+"', '"+str(status)+"', '"+str(grand_price)+"', '"+str(total_discount)+"', '"+str(net_total)+"', '"+str(order_date)+"', '"+str(first_date_str)+"', '"+str(first_date_str)+"', '"+str(note)+"', '"+str(customer_id)+"','"+str(phone)+"','"+str(customer_name)+"','"+str(gender)+"','"+str(age)+"','"+str(customer_category)+"','"+str(staff_id)+"');" 
                insert_sm_invoice_head_counter = db.executesql(insert_sm_invoice_head_counter_sql)


        delete_sm_order_counter_temp_sql = "DELETE from sm_order_head_counter_temp where cid = '"+c_id+"'  AND depot_id ='"+str(depot_id)+"' AND order_sl_counter = '"+get_order_sl+"';"
        delete_sm_order_counter_temp = db.executesql(delete_sm_order_counter_temp_sql)

        select_sm_order_counter_temp_record_sql = "SELECT * FROM sm_order_counter_temp where cid = '"+c_id+"'  AND depot_id ='"+str(depot_id)+"' AND order_sl_counter = '"+get_order_sl+"'"
        select_sm_order_counter_temp_record = db.executesql(select_sm_order_counter_temp_record_sql, as_dict=True)

        for items in range(len(select_sm_order_counter_temp_record)):
            item_records = select_sm_order_counter_temp_record[items]
            depot_id = str(item_records['depot_id'])
            depot_name = str(item_records['depot_name'])
            physician_id = str(item_records['physician_id'])
            physician_name = str(item_records['physician_name'])
            discount_type = str(item_records['discount_type'])
            order_sl_counter = str(item_records['order_sl_counter'])
            order_date = str(item_records['order_date'])
            order_datetime = str(item_records['order_datetime'])
            item_id = str(item_records['item_id'])
            item_name = str(item_records['item_name'])
            quantity = item_records['quantity']
            price = str(item_records['price'])
            item_discount = str(item_records['item_discount'])
            total_price = str(item_records['total_price'])

            insert_sm_order_counter_sql = "INSERT INTO sm_order_counter (cid, depot_id, depot_name, order_sl_counter, order_date, order_datetime, delivery_date, collection_date, physician_id, physician_name, status, ym_date, discount_type, item_id, item_name, quantity, price, item_discount_percent, total_price ) VALUES ('" + str(c_id) + "','" + str(depot_id) + "','" + str(depot_name) + "','" + order_sl_counter + "','" + str(order_date) + "', '"+str(current_datetime)+"',  '" + str(order_date) + "', '"+str(order_date)+"', '"+str(physician_id)+"','" + str(physician_name) + "', '" + str(temp_status) + "', '"+str(first_date_str)+"', '" + str(discount_type) + "','" + str(item_id) + "','" + str(item_name) + "'," + str(quantity) + "," + str(price) + "," + str(item_discount) + "," + str(total_price) + ");"
            insert_sm_order_counter = db.executesql(insert_sm_order_counter_sql)

            insert_sm_invoice_counter_sql = "INSERT INTO sm_invoice_counter (cid, depot_id, depot_name, order_sl_counter, order_date, order_datetime, delivery_date, ym_date, invoice_ym_date, status,  physician_id, physician_name, invoice_date, discount_type, item_id, item_name, actual_tp, quantity, price,  item_discount_percent, total_price) VALUES ('" + str(c_id) + "','" + str(depot_id) + "','" + str(depot_name) + "','" + order_sl_counter + "','" + str(order_date) + "', '"+str(current_datetime)+"', '" + str(order_date) + "', '"+str(first_date_str)+"', '" + str(first_date_str) + "', '"+str(status)+"','"+str(physician_id)+"','" + str(physician_name) + "','" + str(order_date) + "','" + str(discount_type) + "','" + str(item_id) + "','" + str(item_name) + "'," + str(price) + "," + str(quantity) + "," + str(price) + "," + str(item_discount) + "," + str(total_price) + ");"
            insert_sm_invoice_counter = db.executesql(insert_sm_invoice_counter_sql)

            get_item_record_sql = "SELECT a.quantity, a.counter_qty, b.item_per_unit from sm_depot_stock_balance as a INNER JOIN sm_item as b on a.item_id = b.item_id where a.depot_id ='"+str(depot_id)+"' and a.store_name ='Commercial' and b.item_id ='"+str(item_id)+"' LIMIT 1 ; "
            get_item_record = db.executesql(get_item_record_sql, as_dict=True)
            for q in range(len(get_item_record)):
                item_qty_records = get_item_record[q]
                depot_qty = item_qty_records['quantity']
                counter_qty = item_qty_records['counter_qty']
                item_per_unit = item_qty_records['item_per_unit']

            if quantity > counter_qty:
                total_stock_qty = int(counter_qty) + (int(depot_qty) * int(item_per_unit))
                update_stock_qty = total_stock_qty - quantity
                update_depot_stock_qty = int(int(update_stock_qty) / int(item_per_unit))
                updated_counter_qty = int(update_stock_qty) % int(item_per_unit)

                update_sm_depot_stock_balance_sql = "UPDATE sm_depot_stock_balance Set quantity = '"+str(update_depot_stock_qty)+"', counter_qty = '"+str(updated_counter_qty)+"' WHERE cid ='"+c_id+"' AND depot_id ='"+str(depot_id)+"' AND item_id = '"+str(item_id)+"' and store_name ='Commercial'  LIMIT 1; "  
                update_sm_depot_stock_balance = db.executesql(update_sm_depot_stock_balance_sql)
                depot_qty_insert = int(quantity) / int(item_per_unit)


            elif quantity <= counter_qty:
                update_sm_depot_stock_balance_sql = "UPDATE sm_depot_stock_balance Set counter_qty = counter_qty - '"+str(quantity)+"' WHERE cid ='"+c_id+"' AND depot_id ='"+str(depot_id)+"' AND item_id = '"+str(item_id)+"' and store_name ='Commercial'  LIMIT 1; "  
                update_sm_depot_stock_balance = db.executesql(update_sm_depot_stock_balance_sql)
                depot_qty_insert = 0

            t_slRecords_sql = "SELECT id,t_sl FROM counter_market_transaction WHERE cid='" + c_id + "' AND depot_id='" + depot_id + "' order by id desc LIMIT 1;"
            t_slRecords = db.executesql(t_slRecords_sql, as_dict=True)
            for l in range(len(t_slRecords)):
                depotRecords_v = t_slRecords[l]
                row_id = str(depotRecords_v['id'])
                t_sl = depotRecords_v['t_sl']
                t_sl_v=t_sl+1

            search_type = 'Depot_to_counter'
            insert_counter_to_market_sql = "INSERT INTO counter_market_transaction(cid, t_sl, depot_id, depot_name, item_id, item_name, transaction_type, Item_per_unit, qty, counter_qty, transaction_date) VALUES ('"+str(c_id)+"', '"+str(t_sl_v)+"', '"+str(depot_id)+"', '"+str(depot_name)+"','"+str(item_id)+"','"+str(item_name)+"','"+str(search_type)+"','"+str(item_per_unit)+"', '"+str(depot_qty_insert)+"', '"+str(quantity)+"', '"+str(current_datetime)+"')"
            insert_counter_to_market = db.executesql(insert_counter_to_market_sql)

        delete_sql = "DELETE from sm_order_counter_temp where cid = '"+c_id+"'  AND depot_id ='"+str(depot_id)+"' and order_sl_counter = '"+get_order_sl+"';"
        records_delete = db.executesql(delete_sql)

        updateDepotRecord = "UPDATE sm_depot SET order_sl_counter='" + str(order_sl) + "' WHERE id='" + depot_row_id + "' AND depot_id ='"+str(depot_id)+"';"
        updateDepotRecord = db.executesql(updateDepotRecord)

        session.sales_date = ''
        session.physician_id = ''
        session.discount_type = ''
        session.customer_id = ''
        session.phone = ''
        session.customer_name = ''
        session.gender = ''
        session.age = ''
        session.staff_id = ''
        session.note = ''
        session.flash = 'Invoiced Successfully'
        redirect (URL('counter','counter_add'))

    #================================ CANCEL BUTTON CLICK =================================#

    if cancel_btn == 'Cancel':
        get_order_sl = request.args(0)
        delete_order_counter_temp_sql = "DELETE from sm_order_counter_temp where cid = '"+c_id+"'  AND depot_id ='"+str(depot_id)+"' AND order_sl_counter = '"+get_order_sl+"';"
        delete_order_counter_temp = db.executesql(delete_order_counter_temp_sql)

        delete_sm_order_head_counter_temp_sql = "DELETE from sm_order_head_counter_temp where cid = '"+c_id+"'  AND depot_id ='"+str(depot_id)+"' AND order_sl_counter = '"+get_order_sl+"';"
        delete_order_head_counter_temp = db.executesql(delete_sm_order_head_counter_temp_sql)

        updateDepotRecord = "UPDATE sm_depot SET order_sl_counter='" + str(order_sl) + "' WHERE id='" + depot_row_id + "';"
        updateDepotRecord = db.executesql(updateDepotRecord)

        session.sales_date = ''
        session.physician_id = ''
        session.discount_type = ''
        session.customer_id = ''
        session.phone = ''
        session.customer_name = ''
        session.gender = ''
        session.age = ''
        session.staff_id = ''
        session.note = ''
        session.flash = 'Canceled Successfully'
        redirect (URL('counter','counter_add'))

    #================================ IMPORT BUTTON CLICK =================================#
    # if import_button == 'Import':
    #     item_id_check = str(request.vars.item_id)
    #     quantity =request.vars.qty_id
    #     stock_qty =request.vars.stock_qty
    #     depot_id = session.depot_id
    #     store_name ='Commercial'
    #     item_per_unit = 1
    #     counter_quantity = 0
    #     # return stock_qty
    #     if quantity == '0' or quantity == 0:
    #         session.flash = 'Quantity should not be 0'
    #         redirect(URL(c='counter',f='counter_add'))
    #     else:
    #         if int(quantity) <= int(stock_qty):
    #             session.flash = 'Stock Already Available'
    #             redirect(URL(c='counter',f='counter_add'))
    #         else:
    #             try:
    #                 item_id =str(request.vars.item_id).strip().split('|')[0]
    #                 item_name =str(request.vars.item_id).strip().split('|')[1]
    #             except:
    #                 item_id = ''
    #                 item_name = ''

    #             check_item_qty_sql = "SELECT quantity,counter_qty from sm_depot_stock_balance where cid = '"+c_id+"' and depot_id ='"+str(depot_id)+"' and item_id ='"+str(item_id)+"' and store_name ='Commercial' LIMIT 1;"
    #             check_item_qty = db.executesql(check_item_qty_sql, as_dict=True)
    #             for q in range(len(check_item_qty)):
    #                 records_dict=check_item_qty[q]
    #                 depot_stock_qty = records_dict["quantity"]
    #                 counter_stock_qty = records_dict["counter_qty"]


    #             if int(quantity) > int(counter_stock_qty):
    #             #     session.flash = 'Quantity should be lees than Stock quantity'
    #             #     # redirect(URL(c='counter',f='counter_add'))
    #             # else:

    #                 check_exits_item_sql = "SELECT * FROM sm_item where cid = '"+c_id+"' and item_id ='"+str(item_id)+"' group by item_id limit 1 ;"
    #                 check_exits_item = db.executesql(check_exits_item_sql, as_dict=True)
    #                 for item in range(len(check_exits_item)):
    #                     item_records_dict=check_exits_item[item]
    #                     item_per_unit = item_records_dict["item_per_unit"]
    #                 # return counter_stock_qty
    #                 need_import_unit=(int(quantity)-int(counter_stock_qty))/int(item_per_unit)
    #                 # return need_import_unit
    #                 # compare with depot stock qty
    #                 check_depot_stock_sql = "SELECT quantity FROM sm_depot_stock_balance where cid = '"+c_id+"' and store_name='Commercial' and depot_id='"+str(depot_id)+"' and item_id ='"+str(item_id)+"' group by item_id limit 1 ;"
    #                 # return check_depot_stock_sql
    #                 check_depot_stock = db.executesql(check_depot_stock_sql, as_dict=True)
    #                 for depot_stock_item_n in range(len(check_depot_stock)):
    #                     depot_stock_item_dict=check_depot_stock[depot_stock_item_n]
    #                     item_depot_stock_n = depot_stock_item_dict["quantity"]
                        
    #                 # return item_depot_stock_n
                    
    #                 if int(need_import_unit) <= int(item_depot_stock_n):
    #                     pass
    #                 else:
    #                     session.flash = 'Depot stock not Available'
    #                     redirect(URL(c='counter',f='counter_add'))

    #                 counter_quantity = int(item_per_unit) * int(need_import_unit)

    #                 # return need_import_unit
    #                 # return counter_quantity
    #                 update_market_to_counter_sql = "UPDATE sm_depot_stock_balance SET quantity = quantity - '" + str(need_import_unit) + "', counter_qty = counter_qty + '" + str(counter_quantity) + "' WHERE cid = '" + c_id + "' AND depot_id = '" + str(depot_id) + "' AND item_id = '" + str(item_id) + "' and store_name ='Commercial' LIMIT 1"
    #                 update_market_to_counter = db.executesql(update_market_to_counter_sql)
    #                 session.flash = 'Quantity Imported Successfully'
    #                 # redirect(URL(c='counter',f='counter_add'))

    #                 t_slRecords_sql = "SELECT id,t_sl FROM counter_market_transaction WHERE cid='" + c_id + "' AND depot_id='" + depot_id + "' order by id desc LIMIT 1;"
    #                 # return t_slRecords_sql
    #                 t_slRecords = db.executesql(t_slRecords_sql, as_dict=True)
    #                 for l in range(len(t_slRecords)):
    #                     depotRecords_v = t_slRecords[l]
    #                     row_id = str(depotRecords_v['id'])
    #                     t_sl = depotRecords_v['t_sl']
    #                     t_sl_v=t_sl+1

    #                     # return t_sl_v

    #                 search_type = 'Depot_to_counter'
    #                 insert_counter_to_market_sql = "INSERT INTO counter_market_transaction(cid, t_sl, depot_id, depot_name, item_id, item_name, transaction_type, Item_per_unit, qty, counter_qty, transaction_date) VALUES ('"+str(c_id)+"', '"+str(t_sl_v)+"', '"+str(depot_id)+"', '"+str(depot_name)+"','"+str(item_id)+"','"+str(item_name)+"','"+str(search_type)+"','"+str(item_per_unit)+"', '"+str(quantity)+"', '"+str(counter_quantity)+"', '"+str(current_datetime)+"')"
    #                 # return insert_counter_to_market_sql
    #                 insert_counter_to_market = db.executesql(insert_counter_to_market_sql)


    invoice_counter_record_sql = "SELECT id, item_id, item_name, quantity, price, item_discount, total_price, order_sl_counter, order_date  from sm_order_counter_temp WHERE cid ='"+c_id+"' AND depot_id ='"+str(depot_id)+"';"
    invoice_counter_record = db.executesql(invoice_counter_record_sql, as_dict=True)
    
    physicianRows_sql = "SELECT sm_physician.physician_id, sm_physician.physician_name from sm_physician INNER JOIN sm_physician_depot on sm_physician.physician_id = sm_physician_depot.physician_id where sm_physician.cid = '"+c_id+"' and sm_physician_depot.depot_id = '"+str(depot_id)+"' group by sm_physician.physician_id;"
    physicianRows = db.executesql(physicianRows_sql, as_dict=True)

    discount_type_sql = "SELECT discount_type  from sm_discount_type where cid = '"+c_id+"' group by discount_type order by discount_type;"
    discount_type_list = db.executesql(discount_type_sql, as_dict=True)

    return dict(invoice_counter_record =invoice_counter_record, order_sl=order_sl, discount_type_list = discount_type_list, physicianRows =physicianRows)



#======================================= DELETE ITEM  ========================================================

def counter_delete():
    c_id=session.cid
    response.title='Counter Delete'
    record_id = request.args(0)
    order_sl_counter = request.args(1)
    
    delete_sql = "DELETE from sm_order_counter_temp where cid = '"+c_id+"' and id = '"+record_id+"';"
    records = db.executesql(delete_sql)
    check_exits_order_sl_counter_sql = "SELECT order_sl_counter from sm_order_counter_temp where cid = '"+c_id+"' and order_sl_counter = '"+str(order_sl_counter)+"' group by order_sl_counter"
    check_exits_order_sl_counter = db.executesql(check_exits_order_sl_counter_sql, as_dict=True)
    if len(check_exits_order_sl_counter) == 0:
        delete_sm_order_head_counter_temp_sql = "DELETE from sm_order_head_counter_temp where cid = '"+c_id+"' and order_sl_counter = '"+str(order_sl_counter)+"';"
        delete_order_head_counter_temp = db.executesql(delete_sm_order_head_counter_temp_sql)

    session.flash = 'Deleted Successfully'
    redirect (URL('counter','counter_add'))




#============================ AUTO COMPLETE FUNCTION FOR GET STOCK QUANTITY ===================================

def get_stock_qty():
    c_id = session.cid
    recStr = ''
    item_id=request.vars.item_id
    depot_id = session.depot_id
    stock_qty = 0
    quantity = 0
    item_per_unit = 1

    itemPerUnitRows_sql = "SELECT item_per_unit FROM sm_item WHERE cid = '"+c_id+"'  and item_id = '"+str(item_id)+"'  group by item_id limit 1;"
    itemPerUnitRows = db.executesql(itemPerUnitRows_sql, as_dict=True)
    for item in range(len(itemPerUnitRows)):
        records_item_dict=itemPerUnitRows[item]   
        item_per_unit = str(records_item_dict["item_per_unit"])

    itemRows_sql = "SELECT counter_qty,quantity FROM sm_depot_stock_balance WHERE cid = '"+c_id+"' and depot_id = '" + str(depot_id) + "' and item_id = '"+str(item_id)+"' and store_name ='Commercial' group by depot_id,item_id;"
    itemRows = db.executesql(itemRows_sql, as_dict=True)
    for i in range(len(itemRows)):
        records_ov_dict=itemRows[i]   
        stock_qty = str(records_ov_dict["counter_qty"])
        quantity = str(records_ov_dict["quantity"])
        if recStr == '':
            recStr = stock_qty+'|'+quantity+'|'+item_per_unit
        else:
            recStr += ',' +stock_qty+'|'+quantity+'|'+item_per_unit
    
    return recStr

#============================ AUTO COMPLETE FUNCTION FOR GET STOCK QUANTITY ===================================

def physician_list_depot_wise():
    c_id = session.cid
    depot_id = session.depot_id
    retStr = ''

    physicianRows_sql = "SELECT sm_physician.physician_id, sm_physician.physician_name from sm_physician INNER JOIN sm_physician_depot on sm_physician.physician_id = sm_physician_depot.physician_id where sm_physician.cid = '"+c_id+"' and sm_physician_depot.depot_id = '"+str(depot_id)+"' group by sm_physician.physician_id;"
    physicianRows = db.executesql(physicianRows_sql, as_dict=True)
    for i in range(len(physicianRows)):
        records_ov_dict=physicianRows[i]   
        physician_id=str(records_ov_dict["physician_id"])
        physician_name=str(records_ov_dict["physician_name"])
        if retStr == '':
            retStr = physician_id+'|'+physician_name
        else:
            retStr += ',' +physician_id+'|'+physician_name
    
    return retStr


#============================ AUTO COMPLETE FUNCTION FOR GET COUNTER CUSTOMER PHONE NUMBER ===================================

def get_customer_phone_num():
    c_id = session.cid
    recStr = ''
    depot_id = session.depot_id
    customer_phoneRows_sql = "SELECT phone from counter_customer where cid = '"+c_id+"' group by depot_id,phone;"
    customer_phoneRows = db.executesql(customer_phoneRows_sql, as_dict=True)
    for c in range(len(customer_phoneRows)):
        records_ov_dict=customer_phoneRows[c]   
        phone = str(records_ov_dict["phone"])

        if recStr == '':
            recStr = phone
        else:
            recStr += ',' +phone
    
    return recStr



#============================ AUTO COMPLETE FUNCTION FOR GET COUNTER CUSTOMER NAME, GENDER, AGE ===================================

def get_customer_info():
    c_id = session.cid
    recStr = ''
    phone_num=request.vars.phone
    depot_id = session.depot_id
    customer_info_sql = "SELECT customer_id, customer_name, gender, age from counter_customer where cid = '"+c_id+"'  and phone = '"+str(phone_num)+"'  group by depot_id,phone limit 1;"
    customer_info = db.executesql(customer_info_sql, as_dict=True)
    for i in range(len(customer_info)):
        records_ov_dict=customer_info[i]   
        customer_id = str(records_ov_dict["customer_id"])
        customer_name = str(records_ov_dict["customer_name"])
        gender = str(records_ov_dict["gender"])
        age = str(records_ov_dict["age"])

        if recStr == '':
            recStr = customer_name+'|'+gender+'|'+age+'|'+customer_id
        else:
            recStr += ',' +customer_name+'|'+gender+'|'+age+'|'+customer_id
    
    return recStr



#============================ AUTO COMPLETE FUNCTION FOR GET HAMDARD STAFF LIST ===================================

def get_staff_list():
    c_id = session.cid
    recStr = ''
    depot_id = session.depot_id
    staffRows_sql = "SELECT staff_id from counter_customer where cid = '"+c_id+"' group by staff_id;"
    staffRows = db.executesql(staffRows_sql, as_dict=True)
    for s in range(len(staffRows)):
        records_ov_dict=staffRows[s]   
        staff_id = str(records_ov_dict["staff_id"])

        if recStr == '':
            recStr = staff_id
        else:
            recStr += ',' +staff_id
    
    return recStr




#======================== AUTO COMPLETE FUNCTION FOR GET COUNTER CUSTOMER ID, PHONE, NAME, GENDER, AGE =========================

def get_customer_info_by_staff():
    c_id = session.cid
    recStr = ''
    depot_id = session.depot_id
    staff_id=request.vars.staff_id
    if staff_id == '' :
        staff_id = 'invalid'
    customer_all_info_sql = "SELECT customer_id, phone, customer_name, gender, age from counter_customer where cid = '"+c_id+"' and staff_id = '"+str(staff_id)+"'  group by staff_id limit 1;"
    customer_all_info = db.executesql(customer_all_info_sql, as_dict=True)
    for i in range(len(customer_all_info)):
        records_ov_dict_data=customer_all_info[i]   
        customer_id = str(records_ov_dict_data["customer_id"])
        phone = str(records_ov_dict_data["phone"])
        customer_name = str(records_ov_dict_data["customer_name"])
        gender = str(records_ov_dict_data["gender"])
        age = str(records_ov_dict_data["age"])

        if recStr == '':
            recStr = customer_id+'|'+ phone+'|'+customer_name+'|'+gender+'|'+age
        else:
            recStr += ',' +customer_id+'|'+ phone+'|'+customer_name+'|'+gender+'|'+age
    
    return recStr
