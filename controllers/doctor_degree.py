                   
                    #### ADD DEGREE ######

def degree_add():  

    # if ((session.cid==None) or (session.cid=='None')):
    #     redirect(URL('default','index'))
    response.title='Degree Add'
    submit=request.vars.submit
    c_id=session.cid
    search_value=str(request.vars.searchValue_OpName).strip().replace('None','')
    session.search_value = search_value
    filter_button = str(request.vars.btn_filter).strip()
    all_button = str(request.vars.btn_all).strip()
    degree_condition=''

    doc_type_record_sql = "SELECT doc_type_name from doc_type where cid = '"+c_id+"' group by doc_type_name"
    doc_type_record = db.executesql(doc_type_record_sql, as_dict = True)

    if submit:
        degree_id=request.vars.degree_id
        degree_name= str(request.vars.degree_name).upper().split(',')[0]
        doctor_type= str(request.vars.doctor_type).replace('None', '')
        # return degree_name
        if degree_id!='' and degree_name!='':
            check_degree_sql = "select degree_id, degree_name from doc_degree where cid = '"+c_id+"' and  degree_id='"+str(degree_id)+"' and degree_name = '"+str(degree_name)+"';"
            # return check_degree_sql
            checkdegreeRows = db.executesql(check_degree_sql, as_dict=True)
            if len(checkdegreeRows) > 0:
                response.flash = 'Degree already exists'
               
            else:
                insertdegree_sql = "INSERT INTO doc_degree (`cid`,`degree_id`, `degree_name`, `doc_type_name` ) VALUES ('"+str(c_id)+"',"+degree_id+",'"+str(degree_name)+"', '"+str(doctor_type)+"')"      
                insertdegree = db.executesql(insertdegree_sql)
                response.flash= 'Degree Insert Successfully'
    
    if filter_button == "Filter":
        if session.search_value!='':
            # user_id=search_value.split('|')[0].upper()
            session.degree_name=search_value
            degree_condition = degree_condition+" and degree_name = '"+str(session.search_value)+"' "
            # degreeRows_sql = "SELECT degree_id, degree_name from doc_degree where cid = '"+c_id+"' and  degree_name='"+str(search_value)+"' order by degree_id;"

    if all_button == "All":
        degree_condition = ""
        session.filter_button = None
        session.search_value = ""

    degreeRows_sql = "SELECT degree_id, degree_name, doc_type_name from doc_degree where cid = '"+c_id+"' "+ degree_condition+" order by id desc;"
    degreeRows = db.executesql(degreeRows_sql, as_dict=True)

    session.degree_condition = degree_condition
    return dict(doc_type_record = doc_type_record, degreeRows=degreeRows)


         
def degree_list():
    c_id = session.cid
    retStr = ''

    userRows_sql = "select degree_name from doc_degree where cid = '"+c_id+"' order by degree_name;"
    userRows = db.executesql(userRows_sql, as_dict=True)
    for i in range(len(userRows)):
        records_ov_dict=userRows[i]   
        degree_name=str(records_ov_dict["degree_name"])      
        if retStr == '':
            retStr = degree_name
        else:
            retStr += ',' +degree_name
    
    return retStr


def degree_edit():
    c_id = session.cid
    degree_id = request.args(0)
    degree_name = request.args(1)
    doc_type_name = request.args(2)
    # return doc_type_name
    update_btn=request.vars.update_btn
    btn_delete = request.vars.btn_delete
    doc_type_record_sql = "SELECT doc_type_name from doc_type where cid = '"+c_id+"' group by doc_type_name"
    doc_type_record = db.executesql(doc_type_record_sql, as_dict = True)

    if update_btn:
        degree_ID = request.args(0)
        # return degree_ID
        degree_id = str(request.vars.degree_id).strip()
        degree_name = str(request.vars.degree_name).strip().upper()
        doc_type_name = str(request.vars.doctor_type).strip()
        update_degree_sql= " Update doc_degree Set degree_id= '"+str(degree_id)+"', degree_name= '"+str(degree_name)+"', doc_type_name= '"+str(doc_type_name)+"' where cid = '"+c_id+"' and  degree_id ='"+str(degree_ID)+"' limit 1"  
        # return update_degree_sql
        update_degree = db.executesql(update_degree_sql)
        session.flash = 'Degree Updated Successfully'
        redirect(URL('doctor_degree','degree_add'))

    if btn_delete:
        degree_ID = request.args(0)
        delete_sql = "delete from doc_degree where cid = '"+c_id+"' and degree_id ='"+str(degree_ID)+"' limit 1"
        records = db.executesql(delete_sql)
        session.flash = 'Deleted Successfully'
        redirect(URL('doctor_degree','degree_add'))

    
    return dict(doc_type_record= doc_type_record,degree_id= degree_id, degree_name = degree_name, doc_type_name = doc_type_name)






                    #### DEGREE LIST DOWNLOAD ######

def degree_list_Download():
    c_id = session.cid
    degreeRows_sql = "SELECT degree_id, degree_name, doc_type_name from doc_degree where cid = '"+c_id+"' "+ session.degree_condition+" order by degree_id;"
    degreeRows = db.executesql(degreeRows_sql, as_dict=True)
    myString = 'Degree List\n\n'
    myString += 'Degree ID, Degree Name, Doctor Type\n'
    total=0
    attTime = ''
    totalCount = 0
    for i in range(len(degreeRows)):
        recordsStr = degreeRows[i]
        degree_id = str(recordsStr['degree_id'])
        degree_name = str(recordsStr['degree_name'])
        doc_type_name = str(recordsStr['doc_type_name'])
        
        myString += str(degree_id) + ',' + str(degree_name) + ',' + str(doc_type_name) + '\n'

    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_doctor_degree.csv'
    return str(myString)
