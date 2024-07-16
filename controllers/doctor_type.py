
def doctor_type():  
    if ((session.cid==None) or (session.cid=='None')):
        redirect(URL('default','index'))
    response.title='Doctor Type'
    submit=request.vars.submit
    c_id=session.cid
    search_value=str(request.vars.searchValue_OpName).strip().replace('None','')
    session.search_value = search_value
    filter_button = str(request.vars.btn_filter).strip()
    all_button = str(request.vars.btn_all).strip()
    doctor_type_condition=''
    if submit:
        doctor_type= str(request.vars.doctor_type)

        if doctor_type!='':
            doctor_type_sql = "select  doc_type_name from doc_type where cid = '"+c_id+"' and  doc_type_name ='"+str(doctor_type)+"';"
            doctor_typeRows = db.executesql(doctor_type_sql, as_dict=True)
            if len(doctor_typeRows) > 0:
                response.flash = 'Doctor type already exists'
               
            else:
                insertdiscount_sql = "INSERT INTO doc_type (`cid`,`doc_type_name`) VALUES ('"+str(c_id)+"','"+str(doctor_type)+"')"      
                insertdiscount = db.executesql(insertdiscount_sql)
                response.flash= 'Doctor Type Inserted Successfully'
    

    if filter_button == "Filter":
        # return 'abc'
        if session.search_value!='':
            session.doctor_type=search_value
            doctor_type_condition = doctor_type_condition+" and doc_type_name = '"+str(session.search_value)+"' "

    if all_button == "All":
        doctor_type_condition = ""
        session.filter_button = None
        session.search_value = ""

    doctor_type_SQL = "SELECT id, doc_type_id, doc_type_name from doc_type where cid = '"+c_id+"' "+ doctor_type_condition+" order by id;"
    doctor_type_row = db.executesql(doctor_type_SQL, as_dict=True)

    session.doctor_type_condition = doctor_type_condition

    return dict(doctor_type_row=doctor_type_row)


def doctor_type_edit():
    c_id = session.cid
    btn_delete = request.vars.btn_delete
    update_btn=request.vars.update_btn
    record_id = request.args(0)
    doc_type_name = request.args(1)

    if update_btn:
        record_ID = request.args(0)
        doc_type_edited_value = str(request.vars.doc_type_edited_value)
        update_doc_type_name_sql= " Update doc_type Set doc_type_name= '"+str(doc_type_edited_value)+"' where cid = '"+c_id+"' and  id ='"+str(record_ID)+"' limit 1 "  
        # return update_doc_type_name_sql
        update_update_doc_type_name_sql = db.executesql(update_doc_type_name_sql)
        session.flash = 'Doctor Type Updated Successfully'
        redirect(URL('doctor_type','doctor_type'))

    if btn_delete:
        record_ID = request.args(0)
        delete_sql = "delete from doc_type where cid = '"+c_id+"' and id ='"+str(record_ID)+"' limit 1 "
        records = db.executesql(delete_sql)
        session.flash = 'Deleted Successfully'
        redirect (URL('doctor_type','doctor_type'))

    # return record_ID    
    return dict(record_id= record_id, doc_type_name= doc_type_name)






                    #### PHYSICIAN LIST DOWNLOAD ######

def doctor_type_list():
    c_id = session.cid
    retStr = ''

    userRows_sql = "select doctor_type from sm_doctor_type where cid = '"+c_id+"' order by doctor_type;"
    userRows = db.executesql(userRows_sql, as_dict=True)
    for i in range(len(userRows)):
        records_ov_dict=userRows[i] 
        # doctor_type_id=str(records_ov_dict['doctor_type_id']) 
        doctor_type=str(records_ov_dict['doctor_type'])  
             
        if retStr == '':
            retStr = doctor_type
        else:
            retStr += ',' +doctor_type
    
    return retStr


def doctor_type_Download():
    c_id = session.cid
    doctor_type_SQL = "SELECT * from doc_type where cid = '"+c_id+"' "+ session.doctor_type_condition+" order by id;"
    doctor_type_row = db.executesql(doctor_type_SQL, as_dict=True)
    # return record
    myString = 'Doctor Type List\n\n'
    myString += ' Doctor Type ID, Doctor Type Name\n'
    total=0
    attTime = ''
    totalCount = 0
    for i in range(len(doctor_type_row)):
        recordsStr = doctor_type_row[i]
        doctor_type_id = str(recordsStr['doc_type_id'])
        doc_type_name = str(recordsStr['doc_type_name'])
        
        myString += str(doctor_type_id) + ',' + str(doc_type_name) + ',\n'

    # Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=doctor_type_list.csv'
    return str(myString)



         
