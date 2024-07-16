                  ############### SHOW ALL CLIENT LIST  ################

#    http://127.0.0.1:8000/hamdard/temp_data/client?cid=HAMDARD

def client():
    response.title = 'Client Temp Data' 
    cid=session.cid
    searchValue_client_id = str(request.vars.searchValue_client_id).replace('None','')
    # return searchValue_client_id
    session.searchValue_client_id = searchValue_client_id
    filter_button = str(request.vars.search_btn).strip()
    all_button = str(request.vars.all_btn).strip()
    condition = ''
    # --------------paging
    if len(request.args):
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = 20
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    # return limitby
    # ---------------end paging

    if filter_button == "Filter":
        if session.searchValue_client_id!='':
            client_id=session.searchValue_client_id.split('|')[0].upper()
            # return client_id
            session.client_id=client_id
            condition=condition+" and client_id='"+str(session.client_id)+"'"
    # return condition
    if all_button == "ALL":
        condition = ""
        session.filter_button = ""
        session.searchValue_client_id =""

    client_records_sql = "SELECT client_id, name, status, created_on from sm_client_temp where cid = '"+str(cid)+"' "+condition+" group by client_id order by created_on desc limit %d, %d;" % limitby
    # return client_records_sql
    client_records = db.executesql(client_records_sql, as_dict=True)
    
    ##################### TOTAL COUNT ##############################

    total_record_sql = "select count(id) as total from sm_client_temp WHERE cid='"+str(cid)+"' "
    # return total_record_sql
    total_record = db.executesql(total_record_sql,as_dict = True)
    # total = 0
    for z in range(len(total_record)):
        total_record_str=total_record[z]  
        total=str(total_record_str["total"])

    return dict(client_records=client_records,total = total, page = page, items_per_page = items_per_page)




                  ############### DELETE CLIENT USING ID  ################

def client_delete():
    cid = session.cid
    # return cid
    response.title='Client Delete'
    record_client_id = request.args(0)
    delete_button = str(request.vars.btn_delete).strip()
    # return record_poi_id
    delete_sql = "delete from sm_client_temp where cid = '"+str(cid)+"' and  client_id = '"+record_client_id+"';"
    # return delete_sql
    records = db.executesql(delete_sql)
    session.flash = 'Deleted Successfully'
    redirect (URL('temp_data','client'))




                 ############### SHOW ALL DOCTOR LIST  ################

#    http://127.0.0.1:8000/hamdard/temp_data/client?cid=HAMDARD

def doctor():
    response.title = 'Doctor Temp Data' 
    cid=session.cid
    searchValue_doctor_id = str(request.vars.searchValue_doctor_id).replace('None','')
    # return searchValue_doctor_id
    session.searchValue_doctor_id = searchValue_doctor_id
    filter_button = str(request.vars.search_btn).strip()
    all_button = str(request.vars.all_btn).strip()
    d_condition = ''

    # --------------paging
    if len(request.args):
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = 20
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    # return limitby
    # ---------------end paging

    if filter_button == "Filter":
        if session.searchValue_doctor_id!='':
            doctor_id=session.searchValue_doctor_id.split('|')[0].upper()
            # return doctor_id
            session.doctor_id = doctor_id
            d_condition = d_condition+" and doc_id='"+str(session.doctor_id)+"'"
    # return condition
    if all_button == "ALL":
        condition = ""
        session.filter_button = ""
        session.searchValue_doctor_id =""
   
    doctor_records_sql = "SELECT doc_id, doc_name, status, created_on from sm_doctor_temp where cid = '"+str(cid)+"' "+d_condition+" group by doc_id order by created_on desc limit %d, %d;" % limitby
    # return doctor_records_sql
    doctor_records = db.executesql(doctor_records_sql, as_dict=True)
    
    ##################### TOTAL COUNT ##############################

    total_record_sql = "select count(id) as total from sm_doctor_temp WHERE cid='"+str(cid)+"' "
    # return total_record_sql
    total_record = db.executesql(total_record_sql,as_dict = True)
    # total = 0
    for z in range(len(total_record)):
        total_record_str=total_record[z]  
        total=str(total_record_str["total"])

    return dict(doctor_records=doctor_records,total = total, page = page, items_per_page = items_per_page)




                  ############### DELETE DOCTOR USING ID  ################

def doctor_delete():
    cid = session.cid
    # return cid
    response.title='Doctor Delete'
    record_doc_id = request.args(0)
    delete_button = str(request.vars.btn_delete).strip()
    # return record_poi_id
    delete_sql = "delete from sm_doctor_temp where cid = '"+str(cid)+"' and  doc_id = '"+record_doc_id+"';"
    # return delete_sql
    records = db.executesql(delete_sql)
    session.flash = 'Deleted Successfully'
    redirect (URL('temp_data','doctor'))



                 ######### CLIENT ID AND NAME AUTO COMPLETE USING AJAX ###########

def client_id_list():
    retStr = ''

    client_records_sql = "select client_id, name from sm_client_temp group by client_id order by client_id;"
    # return client_records_sql
    client_record_list = db.executesql(client_records_sql, as_dict=True)
    for i in range(len(client_record_list)):
        records_ov_dict=client_record_list[i]   
        client_id=records_ov_dict["client_id"]   
        name=records_ov_dict["name"]  
        if retStr == '':
            retStr = client_id+'|'+name
        else:
            retStr += ',' +client_id+'|'+name
    
    return retStr



                 ######### DOCTOR ID AND NAME AUTO COMPLETE USING AJAX ###########

def doctor_id_list():
    retStr = ''

    doctor_records_sql = "select doc_id, doc_name from sm_doctor_temp group by doc_id order by doc_id;"
    # return client_records_sql
    doctor_record_list = db.executesql(doctor_records_sql, as_dict=True)
    for i in range(len(doctor_record_list)):
        records_ov_dict=doctor_record_list[i]   
        doc_id=records_ov_dict["doc_id"]   
        name=records_ov_dict["doc_name"]  
        if retStr == '':
            retStr = doc_id+'|'+name
        else:
            retStr += ',' +doc_id+'|'+name
    
    return retStr