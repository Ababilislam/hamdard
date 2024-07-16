
def discount_type():  

    # if ((session.cid==None) or (session.cid=='None')):
    #     redirect(URL('default','index'))
    response.title='Discount Type'
    submit=request.vars.submit
    # return submit
    c_id=session.cid
    # return c_id
    search_value=str(request.vars.searchValue_OpName).strip().replace('None','')
    # return search_value
    session.search_value = search_value
    filter_button = str(request.vars.btn_filter).strip()
    # return filter_button
    all_button = str(request.vars.btn_all).strip()
    # return all_button
    discount_type_condition=''
    if submit:
        # return 'ggg'
        
        # return discount_type_id
        discount_type= str(request.vars.discount_type)
        # return discount_type
        if discount_type!='':
            discount_type_sql = "select discount_type from sm_discount_type where cid = '"+c_id+"' and  discount_type='"+str(discount_type)+"';"
            # return discount_type_sql
            discount_typeRows = db.executesql(discount_type_sql, as_dict=True)
            if len(discount_typeRows) > 0:
                response.flash = 'Discount type/ID already exists'
               
            else:
                insertdiscount_sql = "INSERT INTO sm_discount_type (`cid`,`discount_type`) VALUES ('"+str(c_id)+"','"+str(discount_type)+"')"      
                # return insertdiscount_sql
                insertdiscount = db.executesql(insertdiscount_sql)
                response.flash= 'Discount Type Inserted Successfully'
    

    if filter_button == "Filter":
        # return 'abc'
        if session.search_value!='':
            session.discount_type=search_value
            discount_type_condition = discount_type_condition+" and discount_type = '"+str(session.search_value)+"' "

    if all_button == "All":
        discount_type_condition = ""
        session.filter_button = None
        session.search_value = ""

    discount_type_SQL = "SELECT id, discount_type from sm_discount_type where cid = '"+c_id+"' "+ discount_type_condition+" order by id;"
    # return discount_type_SQL
    discount_type_row = db.executesql(discount_type_SQL, as_dict=True)
    session.discount_type_condition = discount_type_condition
    # return 'abc' 

    return dict(discount_type_row=discount_type_row)


def discount_type_delete():
    # return 'dfghb'
    c_id = session.cid
    # return c_id
    disct_id = request.args(0)
    # return disct_id
    btn_delete = request.vars.btn_delete
    # if btn_delete:
    delete_sql = "delete from sm_discount_type where cid = '"+c_id+"' and id='"+str(disct_id)+"' "
    # return delete_sql
    records = db.executesql(delete_sql)
    session.flash = 'Deleted Successfully'
    redirect (URL('discount_type','discount_type'))



# def discount_type_edit():
#     c_id = session.cid
#     disct_id = request.args(0)
#     discount_type_id = request.args(1)
#     discount_type = request.args(2)
    
#     update_btn=request.vars.update_btn

#     if update_btn:
#         discount_type_id = request.args(1)
#         # return speciality_ID
#         discount_type_id = str(request.vars.discount_type_id).strip()
#         discount_type = str(request.vars.discount_type).strip()
#         update_speciality_sql= " Update sm_discount_type Set discount_type_id= '"+str(discount_type_id)+"', discount_type = '"+str(discount_type)+"' where cid = '"+c_id+"' and  discount_type_id ='"+str(discount_type_id)+"' "  
#         # return update_speciality_sql
#         update_speciality = db.executesql(update_speciality_sql)
#         session.flash = 'Discount Type Updated Successfully'
#         redirect(URL('discount_type','discount_type'))

    
#     return dict(discount_type_id= discount_type_id, discount_type = discount_type)

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


def discount_type_Download():
    c_id = session.cid
    discount_type_SQL = "SELECT id, discount_type from sm_discount_type where cid = '"+c_id+"' "+ session.discount_type_condition+" order by id;"
    discount_type_row = db.executesql(discount_type_SQL, as_dict=True)
    # return record
    myString = 'Discount Type List\n\n'
    myString += ' Discount Type ID, Discount Type\n'
    total=0
    attTime = ''
    totalCount = 0
    for i in range(len(discount_type_row)):
        recordsStr = discount_type_row[i]
        discount_type_id = str(recordsStr['id'])
        discount_type = str(recordsStr['discount_type'])
        
        myString += str(discount_type_id) + ',' + str(discount_type) + ',\n'

    # Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_discount_type.csv'
    return str(myString)



         
