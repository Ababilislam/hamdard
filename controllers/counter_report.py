
# http://127.0.0.1:8000/ipi_report/expense_report_show/expense_report?cid=IBNSINA

# =========================== COUNTER REPORT HOME FUNCTION ========================================#

def counter_report_home():

    cid = session.cid
    depot_id = str(session.depot_id).replace('None','')
    get_depot_physician_list = ''

    if depot_id != '':
        get_depot_physician_list_sql = "SELECT d.physician_id as physician_id, p.physician_name as physician_name FROM sm_physician_depot as d inner join sm_physician as p on d.physician_id = p.physician_id  WHERE d.cid = '"+cid+"' and d.depot_id = '"+str(depot_id)+"' GROUP BY p.physician_id ;"
        get_depot_physician_list = db.executesql(get_depot_physician_list_sql, as_dict = True)
    else:
        get_depot_physician_list_sql = "SELECT d.physician_id as physician_id, p.physician_name as physician_name FROM sm_physician_depot as d inner join sm_physician as p on d.physician_id = p.physician_id  WHERE d.cid = '"+cid+"'  GROUP BY p.physician_id ;"
        get_depot_physician_list = db.executesql(get_depot_physician_list_sql, as_dict = True)

    get_discount_type_rec_sql = "SELECT discount_type FROM sm_discount_type WHERE cid = '"+cid+"' GROUP BY discount_type ;"
    get_discount_type_rec = db.executesql(get_discount_type_rec_sql, as_dict = True)
    
    return dict(get_discount_type_rec = get_discount_type_rec, get_depot_physician_list = get_depot_physician_list)



# ================================ PRODUCT WISE COUNTER REPORT FUNCTION =================================#

def product_wise_report():
    cid = session.cid
    response.title = 'Product Wise Report'
    btn_product_wise_report = str(request.vars.btn_product_wise_report).strip()
    btn_product_wise_report_d = str(request.vars.btn_product_wise_report_d).strip()
  
    btn_product_wise_customer_details = str(request.vars.btn_product_wise_customer_details).strip()
    # # return btn_product_wise_customer_details
    btn_product_wise_customer_details_d = str(request.vars.btn_product_wise_customer_details_d).strip()
    # return btn_product_wise_customer_details
    branch_id=''
    branch_name = ''
    physician_id=''
    physician_name=''
    discount_type_id=''
    status_id=''
    item_id=''
    item_name =''
    from_dt = str(request.vars.from_dt).strip().replace('None','')
    to_dt = str(request.vars.to_dt).strip().replace('None','')

    if session.user_type == 'Admin':
        try:
            branch_id = str(request.vars.branch_id).strip().replace('None','').split('|')[0]
            branch_name = str(request.vars.branch_id).strip().replace('None','').split('|')[1]
        except:
            branch_id=''
            branch_name=''
    else:
        branch_id = str(request.vars.branch_id).strip().replace('None','')

    try:
        physician_id = str(request.vars.physician_id).strip().replace('None','').split('|')[0]
        physician_name= str(request.vars.physician_id).strip().replace('None','').split('|')[1]
    except:
        physician_id=''
        physician_name=''
    discount_type_id = str(request.vars.discount_type_id).strip().replace('None','')
    status_id = str(request.vars.status_id).strip().replace('None','')
    try:
        item_id = str(request.vars.item_id).strip().replace('None','').split('|')[0]
        item_name = str(request.vars.item_id).strip().replace('None','').split('|')[1]
    except:
        item_id=''
        item_name=''
    
    session.from_dt = from_dt
    session.to_dt = to_dt
    session.branch_id = branch_id
    session.physician_id = physician_id
    session.physician_name = physician_name
    session.discount_type_id = discount_type_id
    session.status_id = status_id
    session.item_id = item_id

    condition1 = ''
    condition2 = ''
    if ((from_dt != '') and (to_dt!= '')):
        condition1+= f" AND invoice_date BETWEEN '{from_dt}' AND '{to_dt}'"
        if (branch_id != ''):
            condition1+= "AND depot_id = '"+ str(branch_id) +"'"
        if (physician_id != ''):
            condition1+= " AND physician_id = '"+ str(physician_id) +"'"
        if (discount_type_id != ''):
            condition1+= " AND  discount_type = '"+ str(discount_type_id) +"'"
        if (status_id != ''):
            condition1+= " AND  status = '"+ str(status_id) +"'"
        if (item_id != ''):
            condition2+= " AND  item_id = '"+ str(item_id) +"'"

    rec_str_sql="SELECT *, sum(quantity) as total_quantity FROM sm_invoice_counter WHERE cid = '"+cid+"'  "+condition1+" "+condition2+" group by item_id order by id desc "
    # return rec_str_sql
    recordsCounter=db.executesql(rec_str_sql,as_dict = True)
    
    invoice_head_counter_sql = "SELECT count(order_sl_counter) as invoiced_count, sum(total_amount + discount) as total_amount, sum(discount) as discount_amount FROM sm_invoice_head_counter WHERE cid = '"+cid+"'  "+condition1+" ;"
    invoice_head_counter = db.executesql(invoice_head_counter_sql,as_dict=True)[0]
    invoiced_count = float(str(invoice_head_counter['invoiced_count']).replace('None','0'))
    total_amount = float(str(invoice_head_counter['total_amount']).replace('None','0'))
    discount_amount = float(str(invoice_head_counter['discount_amount']).replace('None','0'))
    
    return_invoice_head_counter_sql = "SELECT count(order_sl_counter) as return_invoiced_count, sum(total_amount + discount) as return_total_amount, sum(discount) as return_discount_amount FROM sm_invoice_head_counter WHERE cid = '"+cid+"'  "+condition1+" AND status LIKE 'Return';"
    return_invoice_head_counter = db.executesql(return_invoice_head_counter_sql,as_dict=True)[0]
    return_invoiced_count = float(str(return_invoice_head_counter['return_invoiced_count']).replace('None','0'))
    return_total_amount = float(str(return_invoice_head_counter['return_total_amount']).replace('None','0'))
    return_discount_amount = float(str(return_invoice_head_counter['return_discount_amount']).replace('None','0'))
    if btn_product_wise_report =='Product Wise Report':
        return dict(recordsCounter=recordsCounter,from_dt=from_dt,to_dt=to_dt,branch_id=branch_id,branch_name=branch_name,physician_id=physician_id,physician_name=physician_name,discount_type_id=discount_type_id,status_id=status_id,item_id=item_id,item_name=item_name,total_amount=total_amount,invoiced_count=invoiced_count,discount_amount=discount_amount,return_invoiced_count=return_invoiced_count,return_total_amount=return_total_amount,return_discount_amount=return_discount_amount)
    if btn_product_wise_report_d != 'None':
        redirect (URL('product_Wise_Report_download',vars=dict(rec_str_sql=rec_str_sql,from_dt=from_dt,to_dt=to_dt,branch_id=branch_id,branch_name=branch_name,physician_id=physician_id,physician_name=physician_name,discount_type_id=discount_type_id,status_id=status_id,item_id=item_id,item_name=item_name,total_amount=total_amount,invoiced_count=invoiced_count,discount_amount=discount_amount,return_invoiced_count=return_invoiced_count,return_total_amount=return_total_amount,return_discount_amount=return_discount_amount)))


    if btn_product_wise_customer_details =='Product Wise Customer Details':
        redirect (URL('product_wise_customer_details',vars=dict(btn_product_wise_customer_details=btn_product_wise_customer_details,from_dt=from_dt,to_dt=to_dt,physician_id=physician_id,physician_name=physician_name,discount_type_id=discount_type_id,status_id=status_id,item_id=item_id,item_name=item_name,branch_id=branch_id,branch_name=branch_name)))
    
    if btn_product_wise_customer_details_d =='D':
        redirect (URL('product_wise_customer_details_download',vars=dict(btn_product_wise_customer_details_d=btn_product_wise_customer_details_d,from_dt=from_dt,to_dt=to_dt,physician_id=physician_id,physician_name=physician_name,discount_type_id=discount_type_id,status_id=status_id,item_id=item_id,item_name=item_name,branch_id=branch_id,branch_name=branch_name)))
    
    return dict(recordsCounter=recordsCounter,from_dt=from_dt,to_dt=to_dt,branch_id=branch_id,branch_name=branch_name,physician_id=physician_id,physician_name=physician_name,discount_type_id=discount_type_id,status_id=status_id,item_id=item_id,item_name=item_name,total_amount=total_amount,invoiced_count=invoiced_count,discount_amount=discount_amount,return_invoiced_count=return_invoiced_count,return_total_amount=return_total_amount,return_discount_amount=return_discount_amount)


# ================================ PRODUCT WISE COUNTER REPORT DOWNLOAD FUNCTION===========================#

def product_Wise_Report_download():
    rec_str_sql = str(request.vars.rec_str_sql)
    recordsCounter=db.executesql(rec_str_sql,as_dict = True)
    from_dt = str(request.vars.from_dt).replace('None','')
    to_dt = str(request.vars.to_dt).replace('None','')
    branch_id = str(request.vars.branch_id).replace('None','')
    branch_name = str(request.vars.branch_name).replace('None','')
    physician_id = str(request.vars.physician_id).replace('None','')
    physician_name = str(request.vars.physician_name).replace('None','')
    discount_type_id = str(request.vars.discount_type_id).replace('None','')
    status_id = str(request.vars.status_id).replace('None','')
    item_id = str(request.vars.item_id).replace('None','')
    item_name = str(request.vars.item_name).replace('None','')
    invoiced_count = str(request.vars.invoiced_count)
    total_amount = str(request.vars.total_amount)
    discount_amount = str(request.vars.discount_amount)
    
    return_invoiced_count = str(request.vars.return_invoiced_count)
    return_total_amount = str(request.vars.return_total_amount)
    return_discount_amount = str(request.vars.return_discount_amount)
    box = 0
    strip = 0
    myString = 'Product Wise Report\n\n'
    myString += f'Date Range : ,{from_dt} ,To : ,{to_dt}\n'
    myString += f'Physician : ,{physician_id}|{physician_name} , Branch : ,{branch_id}|{branch_name}\n'
    myString += f'Discount Type : ,{discount_type_id} , Status : ,{status_id}\n\n'
    myString += 'SL,Item Id,Item Name,Item per/Unit,Qty,Return,Net,Box,Strip\n\n'
    for i in range(len(recordsCounter)):
        recordStr = recordsCounter[i]
        order_sl_counter = str(recordStr['order_sl_counter'])
        item_id = str(recordStr['item_id'])
        item_name = str(recordStr['item_name'])
        quantity = str(recordStr['total_quantity'])
        item_unit = int(get_unit(item_id))
        total_invoice_return = invoice_return(from_dt,to_dt,item_id,branch_id)
        net = int(quantity)-int(total_invoice_return)
        box=int(net/item_unit)
        strip=int(net%item_unit)
        i += 1
        myString += str(i)+','+str(item_id)+','+str(item_name)+','+str(item_unit)+','+str(quantity)+','+ str(total_invoice_return)+','+str(net)+','+str(box)+','+str(strip)+'\n'
    
    myString += "\n\n\n\n , ,Return,Net\n\n"
    myString += str('Invoice Count')+','+str(invoiced_count)+','+str(return_invoiced_count)+','+str(float(invoiced_count)-float(return_invoiced_count))+'\n'
    myString += str('TP Amount')+','+str(total_amount)+','+str(return_total_amount)+','+str(float(total_amount)-float(return_total_amount))+'\n'
    myString += str('Discount Amount')+','+str(discount_amount)+','+str(return_discount_amount)+','+str(float(discount_amount)-float(return_discount_amount))+'\n'
    myString += str('Total Amount')+','+str(float(total_amount)-float(discount_amount))+','+str(float(return_total_amount)-float(return_discount_amount))+','+str((float(total_amount)-float(discount_amount))-float(return_total_amount))+'\n'
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=product_wise_report.csv'
    return str(myString)

    
    
# ================================ GET ITEM PER UNIT FUNCTION ========================================#

def get_unit(item_id):
    item_per_unit_sql =f"select item_per_unit from sm_item where item_id='{item_id}' group by item_id;"
    item_per_unit = db.executesql(item_per_unit_sql,as_dict=True)
    return item_per_unit[0]['item_per_unit']


# ============================== GET INVOICE RETURN QUANTITY FUNCTION =================================#

def invoice_return(from_dt,to_dt,item_id,branch_id):
    condition = ''
    if branch_id:
        condition += f" AND depot_id = '{branch_id}'"
    invoice_return_sql = f"select sum(quantity) as r_quantity from invoice_counter_return where cid = '{session.cid}' AND item_id='{item_id}' {condition} AND invoice_date BETWEEN '{from_dt}' AND  '{to_dt}' group by item_id;"
    invoice_return = db.executesql(invoice_return_sql,as_dict=True)

    try:
        t_invoice_return=invoice_return[0]['r_quantity']
        return t_invoice_return
    except:
        t_invoice_return = 0
        return t_invoice_return
    
    
    
def product_wise_customer_details():
    
    cid = session.cid
    response.title = 'Product Wise Customer Details'
    # cid = request.vars.cid
    # from_dt=str(request.vars.from_dt)
    # to_dt=str(request.vars.to_dt)
    # return to_dt
    btn_product_wise_customer_details = str(request.vars.btn_product_wise_customer_details).strip()
    # condition1=str(request.vars.condition1)
    # return condition1

    branch_id=''
    branch_name = ''
    physician_id=''
    physician_name=''
    discount_type_id=''
    status_id=''
    item_id=''
    item_name =''
    limit_by = 0
    from_dt = str(request.vars.from_dt).strip().replace('None','')
    to_dt = str(request.vars.to_dt).strip().replace('None','')
    
    if session.user_type == 'Admin':
        try:
            branch_id = str(request.vars.branch_id)
            branch_name = str(request.vars.branch_name)
        except:
            branch_id=''
            branch_name=''
    else:
        branch_id = str(request.vars.branch_id).strip().replace('None','')

    try:
        physician_id = str(request.vars.physician_id)
        physician_name= str(request.vars.physician_name)
    except:
        physician_id=''
        physician_name=''
    
    # return physician_id, physician_name
    discount_type_id = str(request.vars.discount_type_id).strip().replace('None','')
    status_id = str(request.vars.status_id).strip().replace('None','')
    # return status_id
    try:
        item_id = str(request.vars.item_id)
        item_name = str(request.vars.item_name)
        
    except:
        item_id=''
        item_name=''
    # item_id = str(request.vars.item_id).strip().replace('None','').split('|')[0]
    # return item_id
    session.from_dt = from_dt
    session.to_dt = to_dt
    session.branch_id = branch_id
    session.physician_id = physician_id
    session.physician_name = physician_name
    session.discount_type_id = discount_type_id
    session.status_id = status_id
    session.item_id = item_id

    condition1 = ''
    if ((from_dt != '') and (to_dt!= '')):
        condition1+= " AND c.invoice_date >= '" + str(from_dt) + "' AND c.invoice_date <= '" + str(to_dt) + "' "
        if (branch_id != ''):
            condition1+= "AND c.depot_id = '"+ str(branch_id) +"'"
        if (physician_id != ''):
            condition1+= " AND c.physician_id = '"+ str(physician_id) +"'"
        if (discount_type_id != ''):
            condition1+= " AND  c.discount_type = '"+ str(discount_type_id) +"'"
        if (status_id != ''):
            condition1+= " AND  c.status = '"+ str(status_id) +"'"
        if (item_id != ''):
            condition1+= " AND  c.item_id = '"+ str(item_id) +"'"


    # return condition2
    
    #========================= PAGING ==============================
    if len(request.args):
        page_Number = int(request.args[0])
    else:
        page_Number = 0
    item_per_page = 100
    if page_Number is not None and item_per_page is not None:
        # limit_by = ((page_Number + 1) * item_per_page , item_per_page )
        limit_by = (page_Number * item_per_page,  item_per_page + 1)
    limit_start, limit_end = limit_by
#========================= PAGING ==============================
   
    #=====================query================================
    invoice_sql= f"""
    SELECT 
        c.order_sl_counter,
        c.invoice_date,
        c.depot_id,
        c.depot_name,
        c.physician_id,
        c.physician_name,
        h.customer_id,
        h.customer_name,
        c.item_id,
        c.item_name,
        c.status,
        c.discount_type,
        c.item_discount_percent,
        i.price,
		(i.price/i.item_per_unit) as price_per_unit,
		i.item_per_unit  AS item_per_unit,
		c.quantity,
        
        c.total_price as gross_amount,
 
        ((c.item_discount_percent/100)*(c.actual_tp*c.quantity)) as dis_amnt
              
    FROM 
	sm_item i, sm_invoice_counter c,sm_invoice_head_counter h
    WHERE
        i.cid = c.cid AND i.item_id = c.item_id AND c.cid = '{cid}'
        And c.depot_id=h.depot_id 
         {condition1}
    GROUP BY
        c.item_id,
        c.depot_id,
        c.order_sl_counter
    ORDER BY 
    c.id 
    DESC 
    LIMIT %d, %d""" % (limit_start, limit_end)
  
    
    # return invoice_sql

    invoice_sql_execute=db.executesql(invoice_sql,as_dict = True)

    return dict(btn_product_wise_customer_details=btn_product_wise_customer_details,invoice_sql_execute=invoice_sql_execute,from_dt=from_dt,to_dt=to_dt,branch_id=branch_id,branch_name=branch_name,physician_id=physician_id,physician_name=physician_name,item_id=item_id,item_name=item_name,discount_type_id=discount_type_id,status_id=status_id, page_Number=page_Number, item_per_page = item_per_page)


def product_wise_customer_details_download():
    
    cid = session.cid
    # cid = request.vars.cid
    from_dt=str(request.vars.from_dt)
    to_dt=str(request.vars.to_dt)
    # return to_dt
    
    btn_product_wise_customer_details_d=str(request.vars.btn_product_wise_customer_details_d).strip()
    
    branch_id=''
    branch_name = ''
    physician_id=''
    physician_name=''
    discount_type_id=''
    status_id=''
    item_id=''
    item_name =''
    from_dt = str(request.vars.from_dt).strip().replace('None','')
    to_dt = str(request.vars.to_dt).strip().replace('None','')
    
    if session.user_type == 'Admin':
        try:
            branch_id = str(request.vars.branch_id)
            branch_name = str(request.vars.branch_id)
        except:
            branch_id=''
            branch_name=''
    else:
        branch_id = str(request.vars.branch_id).strip().replace('None','')

    try:
        physician_id = str(request.vars.physician_id)
        physician_name= str(request.vars.physician_name)
    except:
        physician_id=''
        physician_name=''
    
    # return physician_id, physician_name
    discount_type_id = str(request.vars.discount_type_id).strip().replace('None','')
    status_id = str(request.vars.status_id).strip().replace('None','')
    # return status_id
    try:
        item_id = str(request.vars.item_id)
        item_name = str(request.vars.item_name)
        
    except:
        item_id=''
        item_name=''
    # item_id = str(request.vars.item_id).strip().replace('None','').split('|')[0]
    # return item_id
    session.from_dt = from_dt
    session.to_dt = to_dt
    session.branch_id = branch_id
    session.physician_id = physician_id
    session.physician_name = physician_name
    session.discount_type_id = discount_type_id
    session.status_id = status_id
    session.item_id = item_id

    condition1 = ''
    if ((from_dt != '') and (to_dt!= '')):
        condition1+= " AND c.invoice_date >= '" + str(from_dt) + "' AND c.invoice_date <= '" + str(to_dt) + "' "
        if (branch_id != ''):
            condition1+= "AND c.depot_id = '"+ str(branch_id) +"'"
        if (physician_id != ''):
            condition1+= " AND c.physician_id = '"+ str(physician_id) +"'"
        if (discount_type_id != ''):
            condition1+= " AND  c.discount_type = '"+ str(discount_type_id) +"'"
        if (status_id != ''):
            condition1+= " AND  c.status = '"+ str(status_id) +"'"
        if (item_id != ''):
            condition1+= " AND  c.item_id = '"+ str(item_id) +"'"

    
    
    
    invoice_sql= f"""
    SELECT 
        c.order_sl_counter,
        c.invoice_date,
        c.depot_id,
        c.depot_name,
        c.physician_id,
        c.physician_name,
        h.customer_id,
        h.customer_name,
        c.item_id,
        c.item_name,
        c.status,
        c.discount_type,
        c.item_discount_percent,
        i.price,
		(i.price/i.item_per_unit) as price_per_unit,
		i.item_per_unit  AS item_per_unit,
		c.quantity,
        
        c.total_price as gross_amount,
 
        ((c.item_discount_percent/100)*(c.actual_tp*c.quantity)) as dis_amnt
               
    FROM 
	sm_item i, sm_invoice_counter c,sm_invoice_head_counter h
    WHERE
        i.cid = c.cid AND i.item_id = c.item_id AND c.cid = '{cid}'
        And c.depot_id=h.depot_id 
         {condition1}
    GROUP BY
        c.item_id,
        c.depot_id,
        c.order_sl_counter
    ORDER BY 
    c.id 
    DESC;"""
    # return invoice_sql
    invoice_sql_execute=db.executesql(invoice_sql,as_dict = True)
    myString = 'product_wise_customer_details\n\n'
    myString += f'Date Range : ,{from_dt} ,To : ,{to_dt}\n'
    myString += f'Physician : ,{physician_id}|{physician_name} , Branch : ,{branch_id}|{branch_name}\n'
    myString += f'Discount Type : ,{discount_type_id} , Status : ,{status_id}, Item :,{item_id}\n\n'
    
    myString += 'SL,inv. Date,inv. SL,B. ID,B. Name, Phy. ID,Pyh. Name,Item ID,Item Name,Status,Discount Type,Discount %,Price,Price per/unit,Item Per/Unit,Qty,Return,Box,Strip,Gross Amount,Dis. Amount,Net. Amount,Cust. ID,Cust. Name\n\n'
    for i in range(len(invoice_sql_execute)):
        
        recordData=invoice_sql_execute[i]
        order_sl=recordData['order_sl_counter']
        depot_id=recordData['depot_id']
        depot_name=recordData['depot_name']
        physician_id=recordData['physician_id']
        physician_name=recordData['physician_name']
        customer_id=recordData['customer_id']
        customer_name=recordData['customer_name']
        item_id=recordData['item_id']
        item_name=recordData['item_name']
        status=recordData['status']
        discount_type=recordData['discount_type']
        price=recordData['price']
        invoice_date=recordData['invoice_date']
        quantity=recordData['quantity']
        quantity1=recordData['quantity']if status=='Invoiced' else 0
        discount=recordData['item_discount_percent']if recordData['item_discount_percent'] is not None else 0
        price_per_unit=recordData['price_per_unit']
        item_per_unit=recordData['item_per_unit']
        return_count=recordData['quantity'] if status=='Return' else 0
        gross_amount1=recordData['gross_amount']if recordData['gross_amount'] is not None else 0
        
        gross_amount=gross_amount1 if return_count == 0 else 0
        dis_amnt1=recordData['dis_amnt']if recordData['dis_amnt'] is not None else 0
        dis_amnt=dis_amnt1 if return_count == 0 else 0
        net_amnt=(gross_amount-dis_amnt )if return_count == 0 else 0
        box=int(quantity/item_per_unit)if return_count == 0 else 0
        strip=(quantity%item_per_unit)if return_count == 0 else 0

        i += 1
        myString += str(i)+','+str(invoice_date)+','+str(order_sl)+','+str(depot_id)+','+str(depot_name)+','+ str(physician_id)+','+str(physician_name)+','+str(item_id)+','+str(item_name)+','+str(status)+','+str(discount_type)+','+str(discount)+','+str(price)+','+str(price_per_unit)+','+str(item_per_unit)+','+str(quantity1)+','+str(return_count)+','+str(box)+','+str(strip)+','+str(gross_amount)+','+str(dis_amnt)+','+str(net_amnt)+','+str(customer_id)+','+str(customer_name)+'\n'    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=product_wise_customer_details.csv'
    return str(myString)    
    