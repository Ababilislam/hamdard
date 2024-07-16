
# http://127.0.0.1:8000/hamdard/auto_delivery_with_tp_rules_test/auto_delivery_start

def auto_delivery_start():
	c_id = 'HAMDARD'
	current_date = date_fixed
	current_date = str(current_date).split(' ')[0]
	select_sm_order_head_record_sql = "SELECT * FROM sm_order_head where cid = '"+c_id+"' and status = 'Submitted' and flag_data = '0' and field1 = 'ORDER' group by sl order by id limit 10 "
	select_sm_order_head_record = db.executesql(select_sm_order_head_record_sql, as_dict=True)

	for item in range(len(select_sm_order_head_record)):
		item_record = select_sm_order_head_record[item]
		depot_id = str(item_record['depot_id'])
		depot_name = str(item_record['depot_name'])
		store_id = str(item_record['store_id'])
		store_name = str(item_record['store_name'])
		sl = str(item_record['sl'])
		client_id = str(item_record['client_id'])
		client_name = str(item_record['client_name'])
		rep_id = str(item_record['rep_id'])
		rep_name = str(item_record['rep_name'])
		order_date = str(item_record['order_date'])
		order_datetime = str(item_record['order_datetime'])
		payment_mode = str(item_record['payment_mode'])
		area_id = str(item_record['area_id'])
		area_name = str(item_record['area_name'])
		ym_date = str(item_record['ym_date'])
		client_cat = str(item_record['client_cat'])
		note = str(item_record['note'])
		market_id = str(item_record['market_id'])
		market_name = str(item_record['market_name'])

		orderRows=db((db.sm_order.cid==c_id) & (db.sm_order.depot_id==depot_id)&(db.sm_order.sl==sl)).select(db.sm_order.ALL,orderby=db.sm_order.item_id)
		if not orderRows:
			ordHRow.update_record(status='Invoiced',flag_data='1',field2=1)
		else:
			detailList=[]
			discount_precent=0
			category_id=''
			select_sm_order_record_sql = "SELECT * FROM sm_order where cid = '"+c_id+"'  AND depot_id ='"+str(depot_id)+"' AND sl = '"+sl+"' group by sl, item_id ;"
			select_sm_order_record = db.executesql(select_sm_order_record_sql, as_dict=True)
			for items in range(len(select_sm_order_record)):
				item_records = select_sm_order_record[items]
				depot_id = str(item_records['depot_id'])
				depot_name = str(item_records['depot_name'])
				order_date = str(item_records['order_date'])
				order_datetime = str(item_records['order_datetime'])
				item_id = str(item_records['item_id'])
				item_name = str(item_records['item_name'])
				category_id = str(item_records['category_id'])
				quantity = item_records['quantity']
				price = str(item_records['price'])
				item_vat = str(item_records['item_vat'])
				item_unit = str(item_records['item_unit'])
				item_carton = str(item_records['item_carton'])

				if category_id=='BASKET_01' or category_id=='BASKET_02' or category_id=='BASKET_03' or category_id=='BASKET_04'  or category_id=='CLINICAL ITEM_01':
					discount_precent=19.25
				if category_id=='F AND C':
					discount_precent=16.67

				session.category_id=category_id
				session.discount_precent=discount_precent

				detailDict={'cid':c_id,'depot_id':depot_id,'depot_name':depot_name,'sl':order_sl,'store_id':store_id,'store_name':store_name,'client_id':client_id,'client_name':client_name,'rep_id':rep_id,'rep_name':rep_name,'market_id':market_id,'market_name':market_name,'order_date':order_date,'order_datetime':order_datetime,'delivery_date':delivery_date,'payment_mode':payment_mode,'area_id':area_id,'area_name':area_name,'order_media':order_media,'ym_date':ym_date,'client_cat':client_cat,'note':note,'item_id':item_id,'item_name':item_name,'category_id':category_id,'quantity':quantity,'price':price,'item_vat':item_vat,'item_unit':item_unit,'item_carton':item_carton}
                detailList.append(detailDict)

            #delete temp
            db((db.sm_tp_rules_temp_process.cid==c_id) & (db.sm_tp_rules_temp_process.depot_id==depot_id)).delete()
                        
            #insert temp
            db.sm_tp_rules_temp_process.bulk_insert(detailList)
            
            #----- call function to create invoice with tp rules
            ret=get_order_to_delivery_detail_rules(c_id,depot_id,order_sl,client_id,order_date)




	# 	check_exits_order_sl_counter_sql = "SELECT order_sl_counter from sm_order_head_counter where cid = '"+c_id+"'  AND depot_id ='"+str(depot_id)+"' AND order_sl_counter = '"+str(order_sl_counter)+"' group by order_sl_counter"
	# 	check_exits_order_sl_counter = db.executesql(check_exits_order_sl_counter_sql, as_dict=True)
	# 	if len(check_exits_order_sl_counter) == 0:
	# 	    insert_sm_order_head_counter_sql = "INSERT INTO sm_order_head_counter (cid, depot_id, depot_name, order_sl_counter, order_date, order_datetime, ym_date, status, physician_id, physician_name, discount_type, note, customer_id, phone, customer_name, gender, age, customer_category, staff_id ) VALUES ('"+str(c_id)+"','"+str(depot_id)+"','"+str(depot_name)+"','"+order_sl_counter+"','"+str(order_date)+"', '"+str(current_datetime)+"', '"+str(first_date_str)+"', '"+str(status)+"','"+str(physician_id)+"','"+str(physician_name)+"','"+str(discount_type)+"','"+str(note)+"','"+str(customer_id)+"','"+str(phone)+"','"+str(customer_name)+"','"+str(gender)+"','"+str(age)+"','"+str(customer_category)+"','"+str(staff_id)+"');" 
	# 	    insert_sm_order_head_counter = db.executesql(insert_sm_order_head_counter_sql)

	# 	check_exits_order_sl_counter_sql = "SELECT order_sl_counter from sm_invoice_head_counter where cid = '"+c_id+"'  AND depot_id ='"+str(depot_id)+"' AND order_sl_counter = '"+str(order_sl_counter)+"' group by order_sl_counter"
	# 	check_exits_order_sl_counter = db.executesql(check_exits_order_sl_counter_sql, as_dict=True)
	# 	if len(check_exits_order_sl_counter) == 0:
	# 	    insert_sm_invoice_head_counter_sql = "INSERT INTO sm_invoice_head_counter (cid, depot_id, depot_name, order_sl_counter, order_date, order_datetime, delivery_date, physician_id, physician_name, discount_type, status, actual_total_tp, discount, total_amount, invoice_date, ym_date, invoice_ym_date, note, customer_id, phone, customer_name, gender, age, customer_category, staff_id) VALUES ('"+str(c_id)+"','"+str(depot_id)+"','"+str(depot_name)+"','"+order_sl_counter+"','"+str(order_date)+"', '"+str(current_datetime)+"', '"+str(order_date)+"', '"+str(physician_id)+"','"+str(physician_name)+"','"+str(discount_type)+"', '"+str(status)+"', '"+str(grand_price)+"', '"+str(total_discount)+"', '"+str(net_total)+"', '"+str(order_date)+"', '"+str(first_date_str)+"', '"+str(first_date_str)+"', '"+str(note)+"', '"+str(customer_id)+"','"+str(phone)+"','"+str(customer_name)+"','"+str(gender)+"','"+str(age)+"','"+str(customer_category)+"','"+str(staff_id)+"');" 
	# 	    insert_sm_invoice_head_counter = db.executesql(insert_sm_invoice_head_counter_sql)


		# delete_sm_order_counter_temp_sql = "DELETE from sm_order_head_counter_temp where cid = '"+c_id+"'  AND depot_id ='"+str(depot_id)+"' AND order_sl_counter = '"+get_order_sl+"';"
		# delete_sm_order_counter_temp = db.executesql(delete_sm_order_counter_temp_sql)

		# select_sm_order_counter_temp_record_sql = "SELECT * FROM sm_order_counter_temp where cid = '"+c_id+"'  AND depot_id ='"+str(depot_id)+"' AND order_sl_counter = '"+get_order_sl+"'"
		# select_sm_order_counter_temp_record = db.executesql(select_sm_order_counter_temp_record_sql, as_dict=True)

		# for items in range(len(select_sm_order_counter_temp_record)):
		#     item_records = select_sm_order_counter_temp_record[items]
		#     depot_id = str(item_records['depot_id'])
		#     depot_name = str(item_records['depot_name'])
		#     physician_id = str(item_records['physician_id'])
		#     physician_name = str(item_records['physician_name'])
		#     discount_type = str(item_records['discount_type'])
		#     order_sl_counter = str(item_records['order_sl_counter'])
		#     order_date = str(item_records['order_date'])
		#     order_datetime = str(item_records['order_datetime'])
		#     item_id = str(item_records['item_id'])
		#     item_name = str(item_records['item_name'])
		#     quantity = item_records['quantity']
		#     price = str(item_records['price'])
		#     item_discount = str(item_records['item_discount'])
		#     total_price = str(item_records['total_price'])

		#     insert_sm_order_counter_sql = "INSERT INTO sm_order_counter (cid, depot_id, depot_name, order_sl_counter, order_date, order_datetime, delivery_date, collection_date, physician_id, physician_name, status, ym_date, discount_type, item_id, item_name, quantity, price, item_discount_percent, total_price ) VALUES ('" + str(c_id) + "','" + str(depot_id) + "','" + str(depot_name) + "','" + order_sl_counter + "','" + str(order_date) + "', '"+str(current_datetime)+"',  '" + str(order_date) + "', '"+str(order_date)+"', '"+str(physician_id)+"','" + str(physician_name) + "', '" + str(temp_status) + "', '"+str(first_date_str)+"', '" + str(discount_type) + "','" + str(item_id) + "','" + str(item_name) + "'," + str(quantity) + "," + str(price) + "," + str(item_discount) + "," + str(total_price) + ");"
		#     insert_sm_order_counter = db.executesql(insert_sm_order_counter_sql)

		#     insert_sm_invoice_counter_sql = "INSERT INTO sm_invoice_counter (cid, depot_id, depot_name, order_sl_counter, order_date, order_datetime, delivery_date, ym_date, invoice_ym_date, status,  physician_id, physician_name, invoice_date, discount_type, item_id, item_name, actual_tp, quantity, price,  item_discount_percent, total_price) VALUES ('" + str(c_id) + "','" + str(depot_id) + "','" + str(depot_name) + "','" + order_sl_counter + "','" + str(order_date) + "', '"+str(current_datetime)+"', '" + str(order_date) + "', '"+str(first_date_str)+"', '" + str(first_date_str) + "', '"+str(status)+"','"+str(physician_id)+"','" + str(physician_name) + "','" + str(order_date) + "','" + str(discount_type) + "','" + str(item_id) + "','" + str(item_name) + "'," + str(price) + "," + str(quantity) + "," + str(price) + "," + str(item_discount) + "," + str(total_price) + ");"
		#     insert_sm_invoice_counter = db.executesql(insert_sm_invoice_counter_sql)
	return 'hello'

