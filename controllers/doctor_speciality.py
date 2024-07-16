                   
                    #### ADD SPECIALITY ######

def speciality_add():  

    # if ((session.cid==None) or (session.cid=='None')):
    #     redirect(URL('default','index'))
    response.title='Speciality Add'
    submit=request.vars.submit
    c_id=session.cid
    search_value=str(request.vars.searchValue_OpName).strip().replace('None','')
    session.search_value = search_value
    filter_button = str(request.vars.btn_filter).strip()
    all_button = str(request.vars.btn_all).strip()
    speciality_condition=''
    if submit:
        speciality_id=request.vars.speciality_id
        speciality_name= str(request.vars.speciality_name).split(',')[0]
        # return speciality_name
        if speciality_id!='' and speciality_name!='':
            check_speciality_sql = "select specialty, sl from doc_speciality where cid = '"+c_id+"' and  sl='"+str(speciality_id)+"' and specialty = '"+str(speciality_name)+"';"
            # return check_speciality_sql
            checkspecialityRows = db.executesql(check_speciality_sql, as_dict=True)
            if len(checkspecialityRows) > 0:
                response.flash = 'Speciality already exists'
               
            else:
                insertspeciality_sql = "INSERT INTO doc_speciality (`cid`,`sl`, `specialty`) VALUES ('"+str(c_id)+"',"+speciality_id+",'"+str(speciality_name)+"')"      
                insertspeciality = db.executesql(insertspeciality_sql)
                response.flash= 'Speciality Insert Successfully'
    

    if filter_button == "Filter":
        if session.search_value!='':
            # user_id=search_value.split('|')[0].upper()
            session.speciality_name=search_value
            speciality_condition = speciality_condition+" and specialty = '"+str(session.search_value)+"' "

    if all_button == "All":
        speciality_condition = ""
        session.filter_button = None
        session.search_value = ""

    specialityRows_SQL = "SELECT sl, specialty from doc_speciality where cid = '"+c_id+"' "+ speciality_condition+" order by sl;"
    specialityRows = db.executesql(specialityRows_SQL, as_dict=True)
    session.speciality_condition = speciality_condition

    return dict(specialityRows=specialityRows)


         
def speciality_list():
    c_id = session.cid
    retStr = ''

    userRows_sql = "select specialty from doc_speciality where cid = '"+c_id+"' order by specialty;"
    userRows = db.executesql(userRows_sql, as_dict=True)
    for i in range(len(userRows)):
        records_ov_dict=userRows[i]   
        speciality_name=str(records_ov_dict["specialty"])      
        if retStr == '':
            retStr = speciality_name
        else:
            retStr += ',' +speciality_name
    
    return retStr



def speciality_delete():
    c_id = session.cid
    specialty_id = request.args(0)
    # return specialty_id
    btn_delete = request.vars.btn_delete
    # if btn_delete:
    delete_sql = "delete from doc_speciality where cid = '"+c_id+"' and sl='"+str(specialty_id)+"' "
    records = db.executesql(delete_sql)
    session.flash = 'Deleted Successfully'
    redirect (URL('doctor_speciality','speciality_add'))



def speciality_edit():
    c_id = session.cid
    speciality_id = request.args(0)
    speciality_name = request.args(1)
    
    update_btn=request.vars.update_btn

    if update_btn:
        speciality_ID = request.args(0)
        # return speciality_ID
        speciality_id = str(request.vars.speciality_id).strip()
        speciality_name = str(request.vars.speciality_name).strip()
        update_speciality_sql= " Update doc_speciality Set sl= '"+str(speciality_id)+"', specialty = '"+str(speciality_name)+"' where cid = '"+c_id+"' and  sl ='"+str(speciality_ID)+"' "  
        # return update_speciality_sql
        update_speciality = db.executesql(update_speciality_sql)
        session.flash = 'Speciality Updated Successfully'
        redirect(URL('doctor_speciality','speciality_add'))

    
    return dict(speciality_id= speciality_id, speciality_name = speciality_name)





                    #### SPECIALITY LIST DOWNLOAD ######

def speciality_list_Download():
    c_id = session.cid
    specialityRows_SQL = "SELECT sl, specialty from doc_speciality where cid = '"+c_id+"' "+ session.speciality_condition+" order by sl;"
    specialityRows = db.executesql(specialityRows_SQL, as_dict=True)
    # return record
    myString = 'Speciality List\n\n'
    myString += 'Speciality ID, Speciality Name\n'
    total=0
    attTime = ''
    totalCount = 0
    for i in range(len(specialityRows)):
        recordsStr = specialityRows[i]
        speciality_id = str(recordsStr['sl'])
        speciality_name = str(recordsStr['specialty'])
        
        myString += str(speciality_id) + ',' + str(speciality_name) + ',\n'

    # Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_doctor_speciality.csv'
    return str(myString)
