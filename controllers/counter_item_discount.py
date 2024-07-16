
def counter_item_discount_add(): 

    response.title='counter_item_discount'
    # return submit
    c_id=session.cid
    submit = str(request.vars.btn_submit).strip()
    # return submit 
    search_value=str(request.vars.searchValue_OpName).strip()
    # return search_value 
    # session.search_value = search_value
    filter_button = str(request.vars.btn_filter).strip()
    # return filter_button
    discount_type1=str(request.vars.discount_type1).strip()
    # session.discount_type1 = discount_type1
    all_button = str(request.vars.btn_all).strip()

    item_condition=''

    if submit=='Save':
        try:
            item_id = str(request.vars.item_id).split('|')[0]
            name= str(request.vars.item_id).split('|')[1]
        except:
            item_id = ''
            name = ''

        discount_type = request.vars.discount_type
        percentage = request.vars.percentage

        if item_id!='':
            check_valid_discount_type_sql = "SELECT discount_type from sm_discount_type where cid = '"+c_id+"' and discount_type = '"+str(discount_type)+"'"
            check_valid_discount_type = db.executesql(check_valid_discount_type_sql, as_dict=True)
            if len(check_valid_discount_type) > 0:
                check_item_sql = "SELECT item_id,name from sm_counter_item_discount where cid = '"+c_id+"' and  item_id='"+str(item_id)+"' and discount_type = '"+str(discount_type)+"' ;"
                checkitemRows = db.executesql(check_item_sql, as_dict=True)
                if len(checkitemRows) > 0:
                    response.flash = 'Item already exists'
                else:
                    insertitem_sql = "INSERT INTO sm_counter_item_discount (cid, item_id, name, discount_type, discount_percentage) VALUES ('"+str(c_id)+"','"+str(item_id)+"','"+str(name)+"','"+str(discount_type)+"','"+str(percentage)+"')"      
                    # return insertitem_sql
                    insertitem = db.executesql(insertitem_sql)
                    response.flash= 'Inserted Successfully'
            else:
                response.flash= 'Please Select Valid Discount Type'
        else:
            response.flash= 'Please Select Valid Item'
    
    if filter_button == "Filter":
        if search_value!='':
            item_id = search_value.split('|')[0].upper()           
            session.item_id = item_id     
            item_condition = item_condition+" and item_id = '"+str(session.item_id)+"'"

        if discount_type1 !='':
            session.discount_type1 = discount_type1
            item_condition = item_condition+ " and discount_type = '"+str(session.discount_type1)+"'"

        session.item_condition = item_condition


#=============================== PAGING STRAT ===================================
    if len(request.args):
        page_Number = int(request.args[0])
    else:
        page_Number = 0

    item_per_page = 20

    if page_Number is not None and item_per_page is not None:

        # limit_by = ((page_Number + 1) * item_per_page , item_per_page )
        limit_by = (page_Number * item_per_page, (page_Number + 1) * item_per_page + 1)

#============================== PAGING END =====================================

    if all_button == "All":
        item_condition = ""
        session.filter_button = None
        session.search_value = ""
        session.item_id = ""
        session.discount_type1=""
        session.item_condition = ""

    if session.item_condition == 'None' or session.item_condition == 'NONE' or session.item_condition == None:
        session.item_condition = ''

    itemdiscountRows_sql = "SELECT id,item_id, name,discount_type,  discount_percentage from sm_counter_item_discount where cid = '"+c_id+"' "+session.item_condition+" order by item_id limit %d, %d" % limit_by
    itemDiscountRows = db.executesql(itemdiscountRows_sql, as_dict=True)

    itemdiscountRows_count_sql = "SELECT id,item_id, name,discount_type, discount_percentage from sm_counter_item_discount where cid = '"+c_id+"' "+session.item_condition+" order by item_id ;"
    itemDiscountRows_count = db.executesql(itemdiscountRows_count_sql, as_dict=True)

    return dict(itemDiscountRows=itemDiscountRows, page_Number=page_Number, item_per_page = item_per_page, itemDiscountRows_count = itemDiscountRows_count)



def item_list():
    c_id=session.cid
    reiStr=''

    itemRows_sql = "select item_id,name from sm_item where cid = '"+c_id+"' and status='active';"
    # return itemRows_sql
    itemRows = db.executesql(itemRows_sql, as_dict=True)
    for i in range(len(itemRows)):
        records_ov_dict=itemRows[i]   
        name=str(records_ov_dict["name"])      
        item_id=str(records_ov_dict["item_id"])   
        if reiStr == '':
            reiStr = item_id+'|'+ name
        else:
            reiStr += ',' +item_id+'|'+ name
    
    return reiStr


         
def discount_type_list():
    c_id = session.cid
    retStr = ''

    userRows_sql = "select discount_type from sm_discount_type where cid = '"+c_id+"' order by discount_type;"
    userRows = db.executesql(userRows_sql, as_dict=True)
    for i in range(len(userRows)):
        records_ov_dict=userRows[i] 
        # discount_type_id=str(records_ov_dict['discount_type_id']) 
        discount_type=str(records_ov_dict['discount_type'])  
             
        if retStr == '':
            retStr = discount_type
        else:
            retStr += ',' +discount_type
    
    return retStr


def counter_item_discount_delete():
    # return 'dfghb'
    c_id = session.cid
    # return c_id
    row_id = request.args(0)
    # return row_id
    btn_delete = request.vars.btn_delete
    # if btn_delete:
    delete_sql = "delete from sm_counter_item_discount where cid = '"+c_id+"' and id = '"+row_id+"' "
    # return delete_sql
    records = db.executesql(delete_sql)
    session.flash = 'Deleted Successfully'
    # session.flash = 'Counter Item Discount Updated Successfully'

    redirect (URL('counter_item_discount','counter_item_discount_add'))


def counter_item_discount_edit():
    c_id = session.cid
    row_id = request.args(0)
    item_id = request.args(1)
    # return row_id
    name = request.args(2)
    discount_type = request.args(3)
    discount_percentage=request.args(4)
    # return discount_percentage
    
    update_btn=request.vars.update_btn

    if update_btn:
        item_id = str(request.vars.item_id).strip()
        discount_type = str(request.vars.discount_type).strip()
        discount_percentage = str(request.vars.discount_percentage).strip()
        update_speciality_sql= " Update sm_counter_item_discount Set discount_percentage = '"+str(discount_percentage)+"' where cid = '"+c_id+"'and id = '"+row_id+"' "  
        # return update_speciality_sql
        update_speciality = db.executesql(update_speciality_sql)
        session.flash = 'Counter Item Discount Updated Successfully'
        redirect(URL('counter_item_discount','counter_item_discount_add'))

    
    return dict(item_id=item_id,name=name,discount_percentage=discount_percentage,discount_type = discount_type,row_id=row_id)

def counter_item_discount_Download():
    Input2=request.vars.Input2
    c_id = session.cid
    counter_discount_SQL = "SELECT item_id, name,  discount_type, discount_percentage from sm_counter_item_discount where cid = '"+c_id+"' "+ session.item_condition+" order by item_id;"
    counter_discount_row = db.executesql(counter_discount_SQL, as_dict=True)
    # return record
    myString = 'Counter Item Discount List\n\n'
    myString += ' Discount Type Item ID, Name, Discount Type, Discount Percentage\n'
    total=0
    attTime = ''
    totalCount = 0
    for i in range(len(counter_discount_row)):
        recordsStr = counter_discount_row[i]
        item_id = str(recordsStr['item_id'])
        name = str(recordsStr['name'])
        discount_type = str(recordsStr['discount_type'])
        discount_percentage = str(recordsStr['discount_percentage'])
        
        myString += str(item_id) + ',' + str(name) + ',' +str(discount_type) + ',' + str(discount_percentage) + ',\n'

    # Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_counter_item_discount.csv'
    return str(myString)




def counter_item_discount_batch_upload():
   
    response.title = 'Counter Discount Item Batch Upload'
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
            if i>=100:
                break
            else:
                row_data=row_list[i]                    
                coloum_list=row_data.split( '\t')
                if len(coloum_list)==4:
                    ffExcel=str(coloum_list[0]).strip().upper()
                    
                    if ffExcel!='':
                        if ffExcel not in ff_list_excel:ff_list_excel
                        ff_list_excel.append(ffExcel)       

        for i in range(total_row):
            if i>=500:
                break
            else:
                row_data=row_list[i]
                coloum_list=row_data.split( '\t')            
            
            if len(coloum_list)!=4:
                error_data=row_data+'(4 columns need in a row)\n'
                error_str=error_str+error_data
                count_error+=1
                continue
            else:
                item_idExcel = str(coloum_list[0]).strip().upper()
                # return employee_idExcel
                nameExcel = str(coloum_list[1]).strip().upper()
                discount_typeExcel = str(coloum_list[2]).strip().upper()               
                discount_percentageExcel = str(coloum_list[3]).strip().upper()               
                    
                if item_idExcel==''or item_idExcel == 'NONE' or item_idExcel=='' or item_idExcel== 'NONE' or nameExcel=='' or nameExcel == 'NONE':
                    error_data=row_data+'(Required all value)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue                    
                
                else:
                    existCheckRows= " select * FROM sm_counter_item_discount WHERE cid='"+str(cid)+"' and item_id = '"+str(item_idExcel)+"' and discount_type = '"+str(discount_typeExcel)+"' LIMIT 0,1"
                    # return existCheckRows
                    existCheck = db.executesql(existCheckRows)

                    if len(existCheck) > 0:
                        error_data=row_data+'(Duplicate Item check)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                    else:
                        try:
                            insert_sql = "INSERT INTO sm_counter_item_discount (cid, item_id, name, discount_type, discount_percentage) VALUES ('"+str(cid)+"','"+str(item_idExcel)+"','"+str(nameExcel)+"', '"+str(discount_typeExcel)+"','"+str(discount_percentageExcel)+"');"
                            # return insert_sql
                            update_ff_list = db.executesql(insert_sql)
                            count_inserted+=1
                        except Exception as e:
                            error_str = 'Please do not insert special charachter.'
                                
        if error_str=='':
            error_str='No error'

    return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)