def branch_costing():
    if ((session.cid == None) or (session.cid == 'None')):
        redirect(URL('default','index'))

    response.title = 'Branch Costing'

    cid = session.cid
    user_id = session.user_id
    depot_id = session.depot_id
    depot_name = session.user_depot_name

    date_from = current_date
    now = datetime.datetime.strptime(current_date, "%Y-%m-%d")
    date_ton = now + datetime.timedelta(days = 1)
    date_to = str(date_ton).split(' ')[0]

    # FIRST DATE OF MONTH
    year = now.year
    month = now.month
    submitted_first_date = datetime.datetime(year, month, 1)
    submitted_first_date_str = submitted_first_date.strftime("%Y-%m-%d")

    # session.from_dt = date_from
    # session.to_date = date_from

    # session.from_dt = ''
    # session.to_date = ''

    # session.branch_value = ''
    # session.category_value = ''
    # session.sub_category_value = ''
    # session.branch_cost_condition = ''
    cost_condition = ''
    # cost_condition = session.branch_cost_condition

    cat_type = ''
    sub_cat_type = ''
    amount = ''

    submit = request.vars.submit_btn
    btn_filter = request.vars.btn_filter
    btn_all = request.vars.btn_all

    reqPage = len(request.args)

    if submit == 'Save':
        ref_number = str(request.vars.ref_number).strip().replace('None','')
        cat_type = str(request.vars.category_type).strip().replace('None','')
        sub_cat_type = str(request.vars.sub_category_type).strip().replace('None','')
        amount = str(request.vars.amount).strip().replace('None','')
        
        if cat_type != '' and sub_cat_type != '' and amount != '':
            get_cost_last_sl = "SELECT sl FROM branch_costing GROUP BY sl DESC LIMIT 1;"
            last_cost_sl = db.executesql(get_cost_last_sl, as_dict = True)
            
            if len(last_cost_sl) == 0:
                last_sl = 0
            else:
                last_sl = last_cost_sl[0]['sl']
                
            current_sl = last_sl + 1
            
            insert_cost_sql = f"INSERT INTO branch_costing (cid, sl, depot_id, depot_name, submitted_by_id, submitted_on_date, submitted_on_datetime, ref_number, cost_cat_id, cost_cat_name, cost_sub_cat_id, cost_sub_cat_name, amount, ym_date, created_by) VALUES ('{cid}','{current_sl}','{depot_id}','{depot_name}','{user_id}','{date_from}','{date_fixed}','{ref_number}','{cat_type}','{cat_type}','{sub_cat_type}','{sub_cat_type}','{amount}','{submitted_first_date_str}','{user_id}');"
            db.executesql(insert_cost_sql)

            session.flash= 'Branch Cost Saved Successfully'
            redirect(URL('branch_costing','branch_costing'))
        
        else:
            session.flash= 'Category, Sub-Category & Amount Required'
            redirect(URL('branch_costing','branch_costing'))
    
    #--------paging
    if reqPage:
        try:
            page = int(request.args[0])
        except ValueError:
            page = 0
    else:
        page = 0
        session.from_dt = ''
        session.to_date = ''
        session.branch_value = ''
        session.category_value = ''
        session.sub_category_value = ''
        session.branch_IdStr = ''
        session.category_IdStr = ''
        session.subcategory_IdStr = ''
        session.branch_cost_condition = cost_condition
    
    items_per_page = session.items_per_page

    if(page==0):
        limitby = (page * items_per_page, (page + 1) * items_per_page)
    else:
        limitby = ((page* items_per_page), items_per_page)
    #--------end paging

    if btn_filter == 'Filter':
        from_dt = str(request.vars.to_dt_2).strip().upper()
        to_date = str(request.vars.to_dt_3).strip().upper()
        
        session.from_dt = from_dt
        session.to_date = to_date

        branch_value = str(request.vars.branch_value).strip().replace('None','')
        category_value = str(request.vars.category_value).strip().replace('None','')
        sub_category_value = str(request.vars.sub_category_value).strip().replace('None','')

        session.branch_value = branch_value
        session.category_value = category_value
        session.sub_category_value = sub_category_value

        if session.from_dt != '' or session.to_date != '':
            cost_condition += f" AND submitted_on_date >= '{str(session.from_dt)}' AND submitted_on_date <= '{str(session.to_date)}'"

        if session.branch_value != '':
            session.branch_value = branch_value

            try: 
                branch_IdStr = str(session.branch_value).split('|')[0]
            except:
                branch_IdStr = ''

            cost_condition += f" AND depot_id = '{str(branch_IdStr)}'"
            session.branch_IdStr = branch_IdStr

        if session.category_value != '':
            session.category_value = category_value
            
            try: 
                category_IdStr = str(session.category_value).split('|')[0]
            except:
                category_IdStr = ''

            cost_condition += f" AND cost_cat_id = '{str(category_IdStr)}'"
            session.category_IdStr = category_IdStr

        if session.sub_category_value != '':
            session.sub_category_value = sub_category_value
            
            try: 
                subcategory_IdStr = str(session.sub_category_value).split('|')[0]
            except:
                subcategory_IdStr = ''

            cost_condition += f" AND cost_sub_cat_id = '{str(subcategory_IdStr)}'"
            session.subcategory_IdStr = subcategory_IdStr

        reqPage = 0
        session.branch_cost_condition = cost_condition
        

    if btn_all:
        cost_condition = ''
        from_dt = ''
        to_date = ''
        # session.btn_filter = None
        # session.btn_all = btn_all
        # session.from_dt = date_from
        # session.to_date = date_from
        session.from_dt = ''
        session.to_date = ''
        session.branch_value = ''
        session.category_value = ''
        session.sub_category_value = ''
        session.branch_IdStr = ''
        session.category_IdStr = ''
        session.subcategory_IdStr = ''
        session.branch_cost_condition = cost_condition
        session.sql = ''
        reqPage = 0


    cost_condition=session.branch_cost_condition

    if cost_condition==None or cost_condition=='None':
        cost_condition=''

    get_branch_cost_sql = f"SELECT * FROM branch_costing WHERE cid = '{cid}' {cost_condition} ORDER BY submitted_on_datetime DESC LIMIT %d, %d;" % limitby
    branch_costRows = db.executesql(get_branch_cost_sql, as_dict=True)

    session.sql = get_branch_cost_sql

    get_category_sql = f"SELECT * FROM cost_category WHERE cid = '{cid}' GROUP BY category_id;"
    categoryRows = db.executesql(get_category_sql, as_dict=True)

    # TOTAL RECORDS COUNT
    total_count = 0

    get_total_sql = f"SELECT COUNT(id) AS total FROM branch_costing WHERE cid = '{cid}' {cost_condition} ORDER BY id ASC;"
    total_rows = db.executesql(get_total_sql, as_dict=True)

    total_count = total_rows[0]['total']

    # TOTAL AMOUNT 
    get_total_amount_sql = f"SELECT SUM(amount) as grand_total FROM branch_costing WHERE cid = '{cid}' {cost_condition};"
    total_amount = db.executesql(get_total_amount_sql, as_dict=True)
    
    whole_total_amount = total_amount[0]['grand_total']


    session.branch_cost_condition = cost_condition

    return dict(categoryRows = categoryRows, branch_costRows = branch_costRows, total_count = total_count, page = page, items_per_page = items_per_page, whole_total_amount = whole_total_amount)



# DOWNLOAD
def download_data():
    cid = session.cid
    
    myString = 'Branch Cost\n\n'
    myString += 'Date,Branch ID,Branch Name,Ref. Number,Cost Category ID,Cost Category Name,Cost Sub-Category ID,Cost Sub-Category Name,Amount\n'

    date = ''
    depot_id = ''
    depot_name = ''
    ref_number = ''
    category_id = ''
    category_name = ''
    subCategory_id = ''
    subCategory_name = ''
    amount = 0

    if session.sql != '' and session.sql != 'None' and session.sql != None:
        data_rec_sql = session.sql
        data_rec = db.executesql(data_rec_sql, as_dict=True)

        if len(data_rec) != 0:
            for i in range(len(data_rec)):
                data = data_rec[i]
                depot_id = data['depot_id']
                depot_name = data['depot_name']
                date = data['submitted_on_date']
                ref_number = data['ref_number']
                category_id = data['cost_cat_id']
                category_name = data['cost_cat_name']
                subCategory_id = data['cost_sub_cat_id']
                subCategory_name = data['cost_sub_cat_name']
                amount = data['amount']

                # Create string for csv download
                myString += str(date)+','+str(depot_id)+','+str(depot_name)+','+str(ref_number)+','+str(category_id)+','+str(category_name)+','+str(subCategory_id)+','+str(subCategory_name)+','+str(amount)+'\n'

    else:
        myString += str(date)+','+str(depot_id)+','+str(depot_name)+','+str(ref_number)+','+str(category_id)+','+str(category_name)+','+str(subCategory_id)+','+str(subCategory_name)+',''\n'
    
    # Save as CSV
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=branch_cost.csv'   
    return str(myString)






# DROPDOWN CATEGORY
def get_categories():
    cid = session.cid
    retStr = ''

    categoryRows_sql = f"SELECT category_name FROM cost_category WHERE cid = '{cid}' GROUP BY category_id ORDER BY category_id;"
    categoryRows = db.executesql(categoryRows_sql, as_dict=True)

    for i in range(len(categoryRows)):
        records_ov_dict = categoryRows[i] 
        category_type = str(records_ov_dict['category_name'])  
            
        if retStr == '':
            retStr = category_type
        else:
            retStr += ',' +category_type
    
    return retStr



# DROPDOWN SUB-CATEGORY
def get_sub_categories():
    cid = session.cid
    retStr = ''

    try:
        category_id = str(request.vars.category_id)
    except:
        category_id = ''

    if category_id != '':
        sub_categoryRows_sql = f"SELECT sub_category_id, sub_category_name FROM cost_sub_category WHERE cid = '{cid}' AND category_id = '{category_id}' GROUP BY category_id, sub_category_id ORDER BY sub_category_id;"
        sub_categoryRows = db.executesql(sub_categoryRows_sql, as_dict=True)
    
    else:
        sub_categoryRows_sql = f"SELECT sub_category_id, sub_category_name FROM cost_sub_category WHERE cid = '{cid}' GROUP BY category_id, sub_category_id ORDER BY sub_category_id;"
        sub_categoryRows = db.executesql(sub_categoryRows_sql, as_dict=True)

    for i in range(len(sub_categoryRows)):
        records_ov_dict = sub_categoryRows[i] 
        sub_category_id = str(records_ov_dict['sub_category_id']) 
        sub_category_name = str(records_ov_dict['sub_category_name'])  
            
        if retStr == '':
            retStr = sub_category_id+'|'+sub_category_name
        else:
            retStr += ',' +sub_category_id+'|'+sub_category_name
    
    return retStr



# AUTO-COMPLETE BRANCH
def get_branch():
    cid = session.cid
    retStr = ''

    branchRows_sql = f"SELECT depot_id, name FROM sm_depot WHERE cid = '{cid}' GROUP BY depot_id;"
    branchRows = db.executesql(branchRows_sql, as_dict=True)

    for i in range(len(branchRows)):
        records_ov_dict = branchRows[i] 
        depot_id = str(records_ov_dict['depot_id']) 
        depot_name = str(records_ov_dict['name'])  
            
        if retStr == '':
            retStr = depot_id+'|'+depot_name
        else:
            retStr += ',' +depot_id+'|'+depot_name
    
    return retStr



# DROPDOWN CATEGORY
def get_Categories():
    cid = session.cid
    retStr = ''

    categoryRows_sql = f"SELECT category_id, category_name FROM cost_category WHERE cid = '{cid}' GROUP BY category_id ORDER BY category_id;"
    categoryRows = db.executesql(categoryRows_sql, as_dict=True)

    for i in range(len(categoryRows)):
        records_ov_dict = categoryRows[i] 
        category_id = str(records_ov_dict['category_id']) 
        category_name = str(records_ov_dict['category_name'])  
            
        if retStr == '':
            retStr = category_id+'|'+category_name
        else:
            retStr += ',' +category_id+'|'+category_name
    
    return retStr



# AUTO-COMPLETE SUB-CATEGORY
def get_subCategories():
    cid = session.cid
    retStr = ''

    sub_categoryRows_sql = f"SELECT sub_category_id, sub_category_name FROM cost_sub_category WHERE cid = '{cid}' GROUP BY category_id, sub_category_id ORDER BY sub_category_id;"
    sub_categoryRows = db.executesql(sub_categoryRows_sql, as_dict=True)

    for i in range(len(sub_categoryRows)):
        records_ov_dict = sub_categoryRows[i] 
        sub_category_id = str(records_ov_dict['sub_category_id']) 
        sub_category_name = str(records_ov_dict['sub_category_name']) 
            
        if retStr == '':
            retStr = sub_category_id+'|'+sub_category_name
        else:
            retStr += ',' +sub_category_id+'|'+sub_category_name
    
    return retStr

