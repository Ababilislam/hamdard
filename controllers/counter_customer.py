  
#============================== COUNTER CUSTOMER LIST SHOW FUNCTION ====================================#

def counter_customer_list():  

    if ((session.cid==None) or (session.cid=='None')):
        redirect(URL('default','index'))
    response.title='Counter Customer'
    c_id=session.cid
    user_type = session.user_type

    depot_ID=str(request.vars.depot_ID).strip().replace('None','')
    from_age=str(request.vars.from_age).strip().replace('None','')
    to_age=str(request.vars.to_age).strip().replace('None','')
    gender=str(request.vars.gender).strip().replace('None','')
    customer_id=str(request.vars.customer_id).strip().replace('None','')

    try:
        depot_ID = str(request.vars.depot_ID).split('|')[0]
        depot_name = str(request.vars.depot_ID).split('|')[1]
    except:
        depot_ID = ''
        depot_name = ''

    session.from_age = from_age
    session.to_age = to_age
    session.gender = gender
    session.customer_id = customer_id

    filter_button = str(request.vars.btn_filter).strip()
    all_button = str(request.vars.btn_all).strip()
    counter_cust_condition =''

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
            counter_cust_condition = counter_cust_condition+" and depot_id = '"+str(depot_ID)+"'"

        if ((session.from_age!='') and (session.to_age!='')):
            counter_cust_condition = counter_cust_condition+" and age >= '"+str(session.from_age)+"' and age <= '"+str(session.to_age)+"'"

        if session.gender != '':
            counter_cust_condition = counter_cust_condition+" and gender = '"+str(session.gender)+"'"

        if session.customer_id != '':
            counter_cust_condition = counter_cust_condition+" and customer_id = '"+str(session.customer_id)+"'"


       
    if all_button == "All":
        counter_cust_condition = ""
        session.filter_button = None
        session.depot_ID = ""
        session.depot_name = ""
        session.from_age = ""
        session.to_age = ""
        session.gender = ""
        session.customer_id = ""


    if user_type == 'Admin':
        counter_customerRows_sql = "SELECT * from counter_customer where cid = '"+c_id+"' "+ counter_cust_condition+"  group by phone,customer_id,depot_id order by id desc limit %d, %d" % limit_by
        counter_customerRows = db.executesql(counter_customerRows_sql, as_dict=True)

        get_total_record_count_sql = "SELECT * from counter_customer where cid = '"+c_id+"' "+ counter_cust_condition+"  group by phone,customer_id,depot_id order by id desc "
        get_total_record_count = db.executesql(get_total_record_count_sql, as_dict=True)

    elif user_type == 'Depot':
        depot_id=session.depot_id
        counter_customerRows_sql = "SELECT * from counter_customer where cid = '"+c_id+"' "+ counter_cust_condition+" and depot_id ='"+str(depot_id)+"'  group by phone,customer_id order by id desc limit %d, %d" % limit_by
        counter_customerRows = db.executesql(counter_customerRows_sql, as_dict=True)

        get_total_record_count_sql = "SELECT * from counter_customer where cid = '"+c_id+"' "+ counter_cust_condition+" and depot_id ='"+str(depot_id)+"'  group by phone,customer_id order by id desc "
        get_total_record_count = db.executesql(get_total_record_count_sql, as_dict=True)

    session.counter_cust_condition = counter_cust_condition
    
    return dict(counter_customerRows=counter_customerRows, page_Number=page_Number, item_per_page = item_per_page, get_total_record_count = get_total_record_count)




#============================== COUNTER CUSTOMER EDIT FUNCTION ====================================#


def counter_customer_edit():
    response.title = 'Counter Customer Edit'
    c_id = session.cid
    record_id = request.args(0)
    customer_id = request.args(1)
    btn_delete = request.vars.btn_delete
    update_btn=request.vars.update_btn

    counter_customer_record_sql = "SELECT * from counter_customer where cid = '"+c_id+"' and id = '"+record_id+"' limit 1"
    counter_customer_record = db.executesql(counter_customer_record_sql, as_dict = True)
    for customer in range(len(counter_customer_record)):
        record = counter_customer_record[customer]
        customer_name=str(record["customer_name"])
        phone=str(record["phone"])
        gender=str(record["gender"])                                         
        age=str(record["age"])
        customer_category=str(record["customer_category"])
        staff_id=str(record["staff_id"])

    if update_btn:
        customer_ID = request.args(0)
        customer_name = str(request.vars.customer_name_btn).strip()
        phone = str(request.vars.phone_btn).strip()
        gender = str(request.vars.gender_btn).strip()
        age = str(request.vars.age_btn).strip()
        customer_category = str(request.vars.customer_category_btn).strip()
        staff_id = str(request.vars.staff_id_btn).strip()
        update_counter_customer_sql= " Update counter_customer Set customer_name= '"+str(customer_name)+"', phone= '"+str(phone)+"', gender= '"+str(gender)+"', age= '"+str(age)+"', customer_category= '"+str(customer_category)+"', staff_id= '"+str(staff_id)+"' where cid = '"+c_id+"' and  id ='"+str(record_id)+"' limit 1"  
        update_physician = db.executesql(update_counter_customer_sql)
        session.flash = 'Counter Customer Updated Successfully'
        redirect(URL('counter_customer','counter_customer_list'))

    if btn_delete:
        customer_ID = request.args(0)
        delete_sql = "delete from counter_customer where cid = '"+c_id+"' and customer_id='"+str(customer_ID)+"' limit 1"
        records = db.executesql(delete_sql)
        session.flash = 'Deleted Successfully'
        redirect (URL('counter_customer','counter_customer_list'))

    
    return dict(record_id = record_id, customer_id = customer_id, customer_name = customer_name, phone = phone, gender = gender, age = age, customer_category=customer_category, staff_id=staff_id)




#======================================= COUNTER CUSTOMER LIST DOWNLOAD =====================================#

def counter_customer_list_Download():
    c_id = session.cid
    user_type = session.user_type
    if user_type == 'Admin':
        counter_customerRows_sql = "SELECT * from counter_customer where cid = '"+c_id+"' "+ session.counter_cust_condition+"  group by customer_id order by id desc"
        counter_customerRows = db.executesql(counter_customerRows_sql, as_dict=True)

    elif user_type == 'Depot':
        depot_id=session.depot_id
        counter_customerRows_sql = "SELECT * from counter_customer where cid = '"+c_id+"' "+ session.counter_cust_condition+" and depot_id ='"+str(depot_id)+"'  group by customer_id order by id desc"
        # return counter_customerRows_sql
        counter_customerRows = db.executesql(counter_customerRows_sql, as_dict=True)

    # return record
    myString = 'Counter Customer List\n\n'
    myString += ' Depot ID, Depot Name, Customer ID, Customer Name, Phone, Gender, Age, Customer Category, Staff ID \n'
    total=0
    attTime = ''
    totalCount = 0
    for i in range(len(counter_customerRows)):
        records_ov_dict=counter_customerRows[i]   
        record_id=str(records_ov_dict["id"])
        depot_id=str(records_ov_dict["depot_id"]) 
        depot_name=str(records_ov_dict["depot_name"])
        customer_id=str(records_ov_dict["customer_id"])
        customer_name=str(records_ov_dict["customer_name"])
        phone=str(records_ov_dict["phone"])
        gender=str(records_ov_dict["gender"])                                         
        age=str(records_ov_dict["age"])
        customer_category=str(records_ov_dict["customer_category"])
        staff_id=records_ov_dict["staff_id"]
        
        myString += str(depot_id) + ',' + str(depot_name) + ',' + str(customer_id) + ',' + str(customer_name) + ',' + str(phone) + ',' + str(gender) + ',' + str(age) + ',' + str(customer_category)+ ',' +str(staff_id)+'\n'

    # Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=counter_customer_list.csv'
    return str(myString)






#============================ AUTO COMPLETE FUNCTION FOR GET COUNTER CUSTOMER ID NAME PHONE NUMBER ===================================

def get_counter_customer_list():
    c_id = session.cid
    user_type = session.user_type
    retStr = ''

    if user_type == 'Admin':
        counter_CustomerRows_sql = "SELECT customer_id, customer_name, phone from counter_customer  where cid = '"+c_id+"' group by customer_id order by customer_id;"
        counter_CustormerRows = db.executesql(counter_CustomerRows_sql, as_dict=True)

    elif user_type == 'Depot':
        depot_id = session.depot_id
        counter_CustomerRows_sql = "SELECT customer_id, customer_name, phone from counter_customer  where cid = '"+c_id+"' and depot_id = '"+str(depot_id)+"'  group by customer_id order by customer_id;"
        counter_CustormerRows = db.executesql(counter_CustomerRows_sql, as_dict=True)

    for i in range(len(counter_CustormerRows)):
        records_ov_dict=counter_CustormerRows[i]   
        customer_id=str(records_ov_dict["customer_id"])
        customer_name=str(records_ov_dict["customer_name"])
        phone=str(records_ov_dict["phone"])
        if retStr == '':
            retStr = customer_id+'|'+customer_name+'|'+ phone
        else:
            retStr += ',' +customer_id+'|'+customer_name+'|'+ phone
    
    return retStr




#============================ COUNTER CUSTOMER BATCH UPLOAD FUNCTION  ===================================#


def counter_customer_batch_upload():
   
    response.title = 'Counter Customer Batch Upload'
    cid=session.cid
    btn_upload=request.vars.btn_upload
    count_inserted=0
    count_error=0
    error_str=''
    total_row=0
            
    if btn_upload=='Upload':
        excel_data=str(request.vars.excel_data)
        inserted_count=0
        error_count=0
        
        row_list=excel_data.split( '\n')
        total_row=len(row_list)
        
        ff_list_exist=[]   
        ff_list_excel=[]
                
        ins_list=[]
        ins_dict={}

        # ----------------------
        for i in range(total_row):
            if i >= 500:
                break
            else:
                row_data=row_list[i]                    
                coloum_list=row_data.split( '\t')
                if len(coloum_list)==6:
                    ffExcel=str(coloum_list[0]).strip().upper()
                    
                    if ffExcel!='':
                        if ffExcel not in ff_list_excel:ff_list_excel
                        ff_list_excel.append(ffExcel)       

        for i in range(total_row):
            if i >= 500:
                break
            else:
                row_data=row_list[i]
                coloum_list=row_data.split( '\t')
            
            if len(coloum_list) != 6:
                error_data = row_data+'(6 columns need in a row)\n'
                error_str = error_str+error_data
                count_error += 1
                continue
            else:
                name_Excel = str(coloum_list[0]).strip()
                # return name_Excel
                phoneExcel = str(coloum_list[1]).strip()
                genderExcel = str(coloum_list[2]).strip()             
                ageExcel = str(coloum_list[3]).strip()
                customer_categoryExcel = str(coloum_list[4]).strip()
                staffExcel = str(coloum_list[5]).strip()
                    
                if name_Excel==''or name_Excel == 'NONE' or name_Excel==None or phoneExcel== None or phoneExcel=='' or phoneExcel == 'NONE' or customer_categoryExcel =='' or customer_categoryExcel == 'NONE' or customer_categoryExcel== None:
                    error_data=row_data+'(Name, Phone, Customer Category Can not be empty)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue                    
                
                else:
                    existCheckRows= " SELECT * FROM counter_customer WHERE cid='"+str(cid)+"' and customer_name = '"+str(name_Excel)+"' and phone = '"+str(phoneExcel)+"' LIMIT 0,1"
                    # return existCheckRows
                    existCheck = db.executesql(existCheckRows)

                    if len(existCheck) > 0:
                        error_data=row_data+'(Duplicate Customer check)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                    else:
                        try:
                            customer_id_sql = "SELECT id,customer_id FROM counter_customer WHERE cid='" + cid + "'  order by id desc LIMIT 1;"
                            customer_Records = db.executesql(customer_id_sql, as_dict=True)

                            for c in range(len(customer_Records)):
                                customerRecordsStr = customer_Records[c]
                                rec_id = str(customerRecordsStr['id'])
                                customer_id = int(customerRecordsStr['customer_id']) + 1

                            phoneExcel = int('88'+phoneExcel)

                            insert_sql = "INSERT INTO counter_customer (cid, customer_id, customer_name, phone, gender, age, customer_category, staff_id ) VALUES ('"+str(cid)+"','"+str(customer_id)+"','"+str(name_Excel)+"','"+str(phoneExcel)+"','"+str(genderExcel)+"','"+str(ageExcel)+"','"+str(customer_categoryExcel)+"','"+str(staffExcel)+"')";
                            update_ff_list = db.executesql(insert_sql)
                            count_inserted+=1

                        except Exception as e:
                            error_str = 'Please do not insert special charachter.'
                                
        if error_str=='':
            error_str='No error'

    return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)