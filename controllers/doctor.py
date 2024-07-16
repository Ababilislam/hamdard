
from random import randint

#---------------------------- ADD
def doctor_list():
    task_id = 'rm_doctor_manage'
    task_id_view = 'rm_doctor_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (access_permission_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))
        
    response.title = 'Doctor'

    c_id = session.cid
    
    #  ---------------filter-------
    btn_filter_doctor = request.vars.btn_filter
    btn_all = request.vars.btn_filter_all
    reqPage = len(request.args)
    if btn_filter_doctor:
        session.btn_filter_doctor = btn_filter_doctor
        session.searchType_doctor = str(request.vars.search_type).strip()
        session.searchValue_doctor = str(request.vars.search_value).strip().upper()
        reqPage = 0
    elif btn_all:
        session.btn_filter_doctor = None
        session.searchType_doctor = None
        session.searchValue_doctor = None
        reqPage = 0

    #--------paging
    if reqPage:
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = session.items_per_page
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    #--------end paging

    qset = db()
    qset = qset(db.sm_doctor.cid == c_id)
    qset = qset(db.sm_doctor_area.cid == c_id)
    qset = qset(db.sm_doctor.doc_id == db.sm_doctor_area.doc_id )
    
    if (session.btn_filter_doctor):

        if (session.searchType_doctor == 'territory_id'):
            searchValue=str(session.searchValue_doctor).split('|')[0]            
            qset = qset(db.sm_doctor_area.area_id  == searchValue)

        elif (session.searchType_doctor == 'DocID'):
            searchValue=str(session.searchValue_doctor).split('|')[0]            
            qset = qset(db.sm_doctor.doc_id == searchValue)
            
        elif (session.searchType_doctor == 'Specialty'):            
            qset = qset(db.sm_doctor.specialty == session.searchValue_doctor)
            
        elif (session.searchType_doctor == 'Status'):
            qset = qset(db.sm_doctor.status == session.searchValue_doctor)
            
        elif (session.searchType_doctor == 'UpdatedBy'):
            qset = qset(db.sm_doctor.updated_by == session.searchValue_doctor)
            
    records = qset.select(db.sm_doctor.id,db.sm_doctor.doc_id,db.sm_doctor.doc_name,db.sm_doctor.specialty,db.sm_doctor.degree,db.sm_doctor.doctors_category,db.sm_doctor.status,db.sm_doctor.updated_by,db.sm_doctor_area.area_id,db.sm_doctor_area.area_name, orderby=db.sm_doctor.doc_id, limitby=limitby)
    # return records
    # return db._lastsql
    recordCount=qset.count()
    
    return dict(records=records,recordCount=recordCount, page=page, items_per_page=items_per_page, access_permission=access_permission)

#---------------------------- ADD VALIDATION
def validation_doctor_add(form):
    randNumber = randint(1001, 9999)

    c_id = session.cid
    doc_id = str(form.vars.doc_id).strip().upper()
    doc_name = str(form.vars.doc_name).replace('|', ' ').strip()
    specialty = str(form.vars.specialty).strip()
    mobile = str(form.vars.mobile).strip()

    if mobile == '':
        mobile = 0
    elif int(mobile) < 0:
        mobile = 0

    #------- check duplicate
    existRows = db((db.sm_doctor.cid == c_id) & (db.sm_doctor.doc_id == doc_id)).select(db.sm_doctor.doc_id, limitby=(0, 1))
    if existRows:
        form.errors.doc_id = 'already exist'
    else:
        form.vars.doc_id = doc_id
        form.vars.doc_name = doc_name
        form.vars.specialty = specialty
        form.vars.mobile = mobile
        form.vars.password = randNumber

#---------------------------- ADD
def doctor_add():
    task_id = 'rm_doctor_manage'
    task_id_view = 'rm_doctor_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (access_permission_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='doctor_list'))

    response.title = 'Doctor'
    
    c_id = session.cid

    #   ---------------------
    db.sm_doctor.specialty.requires = IS_IN_DB(db((db.doc_speciality.cid == session.cid)), db.doc_speciality.specialty, orderby=db.doc_speciality.specialty)
    db.sm_doctor.doctors_category.requires = IS_IN_DB(db((db.doc_catagory.cid == session.cid)), db.doc_catagory.category, orderby=db.doc_catagory.category)

    form = SQLFORM(db.sm_doctor,
                  fields=['doc_id', 'doc_name', 'specialty', 'mobile', 'des', 'status', 'attached_institution', 'designation', 'dob','mar_day', 'doctors_category', 'degree'],
                  submit_button='Save'
                  )


    
    form.vars.cid = c_id
    if form.accepts(request.vars, session, onvalidation=validation_doctor_add):
       response.flash = 'Submitted Successfully'

    #  ---------------filter-------
    btn_filter_doctor = request.vars.btn_filter
    btn_all = request.vars.btn_filter_all
    reqPage = len(request.args)
    if btn_filter_doctor:
        session.btn_filter_doctor = btn_filter_doctor
        session.searchType_doctor = str(request.vars.search_type).strip()
        session.searchValue_doctor = str(request.vars.search_value).strip().upper()
        reqPage = 0
    elif btn_all:
        session.btn_filter_doctor = None
        session.searchType_doctor = None
        session.searchValue_doctor = None
        reqPage = 0

    #--------paging
    if reqPage:
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = session.items_per_page
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    #--------end paging

    qset = db()
    qset = qset(db.sm_doctor.cid == c_id)
    if (session.btn_filter_doctor):
        
        if (session.searchType_doctor == 'DocID'):
            qset = qset(db.sm_doctor.doc_id == session.searchValue_doctor)
            
        elif (session.searchType_doctor == 'Specialty'):
            qset = qset(db.sm_doctor.specialty == session.searchValue_doctor)
            
        elif (session.searchType_doctor == 'MobileNo'):
            qset = qset(db.sm_doctor.mobile == session.searchValue_doctor)
            
        elif (session.searchType_doctor == 'Status'):
            qset = qset(db.sm_doctor.status == session.searchValue_doctor)
        
           
            
    records = qset.select(db.sm_doctor.ALL, orderby=db.sm_doctor.doc_id, limitby=limitby)
    
    return dict(form=form, records=records, page=page, items_per_page=items_per_page, access_permission=access_permission)


#---------------------------- EDIT VALIDATION
def validation_doctor_edit(form):
    c_id = session.cid
    doc_name = str(form.vars.doc_name).replace('|', ' ').strip()
    specialty = str(form.vars.specialty).strip()
    mobile = str(form.vars.mobile).strip()

    if mobile == '':
        mobile = 0
    elif int(mobile) < 0:
        mobile = 0

    #-------------- set form value
    form.vars.doc_name = doc_name
    form.vars.specialty = specialty
    form.vars.mobile = mobile

#---------------------------- EDIT
def doctor_edit():
    task_id = 'rm_doctor_manage'
    access_permission = check_role(task_id)
    if (access_permission == False):
        session.flash = 'Access is Denied !'
        redirect (URL('doctor_list'))

    #   ---------------------
    response.title = 'Doctor -Edit'

    c_id = session.cid

    page = request.args(0)
    rowID = request.args(1)
    docID = request.args(2)

    record = db.sm_doctor(rowID) or redirect(URL('doctor_add'))
    db.sm_doctor.specialty.requires = IS_IN_DB(db((db.doc_speciality.cid == session.cid)), db.doc_speciality.specialty, orderby=db.doc_speciality.specialty)
    db.sm_doctor.doctors_category.requires = IS_IN_DB(db((db.doc_catagory.cid == session.cid)), db.doc_catagory.category, orderby=db.doc_catagory.category)
    
    form = SQLFORM(db.sm_doctor,
                  record=record,
                  deletable=True,
                  fields=['doc_name', 'specialty', 'mobile', 'des', 'status', 'attached_institution', 'designation', 'dob','mar_day', 'doctors_category', 'degree'],
                  submit_button='Update'
                  )
    
    if form.accepts(request.vars, session, onvalidation=validation_doctor_edit):
        response.flash = 'Updated Successfully'
        redirect(URL('doctor_list', args=[page]))
    
    usedFlag=False
    usedRows = db((db.sm_doctor_area.cid == c_id) & (db.sm_doctor_area.doc_id == docID)).select(db.sm_doctor_area.doc_id, limitby=(0, 1))
    if usedRows:
        usedFlag=True
    
    
    return dict(form=form, page=page, docID=docID,usedFlag=usedFlag,rowID=rowID)


#===================================== Download
def download_doctor():
    #----------Task assaign----------
    task_id = 'rm_doctor_manage'
    task_id_view = 'rm_doctor_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (access_permission_view == False):
        redirect (URL('doctor_list'))

    #   ---------------------
    c_id = session.cid

    qset = db()
    qset = qset(db.sm_doctor.cid == c_id)
    qset = qset(db.sm_doctor_area.cid == c_id)
    qset = qset(db.sm_doctor.doc_id == db.sm_doctor_area.doc_id )

    if (session.btn_filter_doctor):
        if (session.searchType_doctor == 'territory_id'):
            searchValue=str(session.searchValue_doctor).split('|')[0]            
            qset = qset(db.sm_doctor_area.area_id  == searchValue)

        elif (session.searchType_doctor == 'DocID'):
            searchValue=str(session.searchValue_doctor).split('|')[0]            
            qset = qset(db.sm_doctor.doc_id == searchValue)
        
        elif (session.searchType_doctor == 'Specialty'):            
            qset = qset(db.sm_doctor.specialty == session.searchValue_doctor)
            
        elif (session.searchType_doctor == 'Status'):
            qset = qset(db.sm_doctor.status == session.searchValue_doctor)

        elif (session.searchType_doctor == 'UpdatedBy'):
            qset = qset(db.sm_doctor.updated_by == session.searchValue_doctor)

    else:
        session.flash = 'Filter Required'
        redirect (URL('doctor_list'))

    # records = qset.select(db.sm_doctor.doc_id, db.sm_doctor.doc_name,db.sm_doctor.specialty, db.sm_doctor.des, db.sm_doctor.degree, db.sm_doctor.attached_institution, db.sm_doctor.designation, db.sm_doctor.dob, db.sm_doctor.mobile, db.sm_doctor.doctors_category,db.sm_doctor.status,db.sm_doctor.updated_by,db.sm_doctor_area.area_id,db.sm_doctor_area.area_name, orderby=db.sm_doctor.doc_id )
    
    records = qset.select(db.sm_doctor.id,db.sm_doctor.doc_id,db.sm_doctor.doc_name,db.sm_doctor.specialty, db.sm_doctor.des, db.sm_doctor.degree, db.sm_doctor.attached_institution, db.sm_doctor.designation, db.sm_doctor.dob, db.sm_doctor.mobile, db.sm_doctor.doctors_category,db.sm_doctor.status,db.sm_doctor.updated_by,db.sm_doctor_area.area_id,db.sm_doctor_area.area_name, orderby=db.sm_doctor.doc_name)
    # return db._lastsql
    # return records
    
    #---------
    myString = 'Doctor List\n\n'
    myString += 'Doctor ID,Name, Territory ID, Territory Name, Specialty,Degree,Chamber Address, Attach Institute,Designation,DOB,Mobile,Doctors Category,Status,Updated By\n'
    for rec in records:
        docId = rec.sm_doctor.doc_id
        docName = rec.sm_doctor.doc_name
        specialty = rec.sm_doctor.specialty
        degree = rec.sm_doctor.degree
        chamberAddress = rec.sm_doctor.des
        attachInstitute = rec.sm_doctor.attached_institution
        designation = rec.sm_doctor.designation
        dob = rec.sm_doctor.dob          
        mobile = rec.sm_doctor.mobile
        doctorsCategory = rec.sm_doctor.doctors_category
        status = rec.sm_doctor.status
        updated_by = rec.sm_doctor.updated_by
        area_id = rec.sm_doctor_area.area_id
        area_name = rec.sm_doctor_area.area_name

        docName = str(docName).replace(',', ' ').replace('\n', ' ')
        specialty = str(specialty).replace(',', '; ').replace('\n', ' ')
        degree = str(degree).replace(',', '; ').replace('\n', ' ')
        chamberAddress = str(chamberAddress).replace(',', '; ').replace('\n', ' ')
        attachInstitute = str(attachInstitute).replace(',', '; ').replace('\n', ' ')
        designation = str(designation).replace(',', '; ').replace('\n', ' ')
        doctorsCategory = str(doctorsCategory).replace(',', '; ').replace('\n', ' ')
        status = str(status).replace(',', '; ').replace(',', ' ').replace('\n', ' ') 
        area_id = str(area_id).replace(',', ' ').replace('\n', ' ')
        area_name = str(area_name).replace(',', ' ').replace('\n', ' ')

        if dob == 'None':
            dob = ''
        # if int(mobile) == 0:
        #     mobile = ''

            
        myString += str(docId)+ ',' + str(docName) + ',' + str(area_id) + ',' + str(area_name)+ ',' + str(specialty)+ ',' + str(degree) + ',' + str(chamberAddress) + ',' + str(attachInstitute) + ',' + str(designation) + ',' + str(dob) + ',' + str(mobile) + ',' + str(doctorsCategory) + ',' + str(status) + ',' + str(updated_by) + '\n'

    #-----------
    # return myString
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_doctor.csv'
    return str(myString)


def batch_upload_doctor():
    task_id = 'rm_doctor_manage'
    access_permission = check_role(task_id)
    if (access_permission == False):
        session.flash = 'Access is Denied !'
        redirect (URL('doctor_list'))

    #----------
    response.title = 'Doctor Batch Upload'

    c_id = session.cid

    btn_upload = request.vars.btn_upload
    count_inserted = 0
    count_error = 0
    error_str = ''
    total_row = 0
    if btn_upload == 'Upload':
        excel_data = str(request.vars.excel_data)
        inserted_count = 0
        error_count = 0
        error_list = []
        row_list = excel_data.split('\n')
        total_row = len(row_list)

        doctor_list_excel = []
        doctor_list_exist = []
        excelList = []

        ins_list = []
        ins_dict = {}

        for i in range(total_row):
            if i >= 100:
                break
            else:
                row_data = row_list[i]
                coloum_list = row_data.split('\t')
                if len(coloum_list) == 10:
                    doctor_list_excel.append(str(coloum_list[0]).strip().upper())

        #  create client list
        existDoctorRows = db((db.sm_doctor.cid == c_id) & (db.sm_doctor.doc_id.belongs(doctor_list_excel))).select(db.sm_doctor.doc_id, orderby=db.sm_doctor.doc_id)
        doctor_list_exist = existDoctorRows.as_list()
        
        #   --------------------
        for i in range(total_row):
            if i >= 500:
                break
            else:
                row_data = row_list[i]
            coloum_list = row_data.split('\t')

            if len(coloum_list) == 10:
                doc_id = str(coloum_list[0]).strip().upper()
                doc_name = str(coloum_list[1]).strip().replace('|', ' ')
                specialty = str(coloum_list[2]).strip()
                degree = str(coloum_list[3]).strip()
                attachInstitute = str(coloum_list[4]).strip()
                designation = str(coloum_list[5]).strip()
                dob = str(coloum_list[6]).strip()   
                mar_day = str(coloum_list[7]).strip()             
                mobile = str(coloum_list[8]).strip()
                doctorsCategory = str(coloum_list[9]).strip()
                status = 'ACTIVE'
                
                if not(doc_id == '' or doc_name == ''):
                    if mobile == '':
                        mobile = 0

                    validMobile = True
                    try:
                        mobile = int(mobile)
                    except:
                        validMobile = False

                    if validMobile == True:
                        
                        dobFlag=True
                        marFlag=True
                        if dob!='':
                            try:                                
                                dob = datetime.datetime.strptime(dob,'%Y-%m-%d')                                
                            except:
                                dobFlag = False
                        if mar_day!='':
                            try:                                
                                mar_day = datetime.datetime.strptime(mar_day,'%Y-%m-%d')                                
                            except:
                                marFlag = False
                        
                        if dobFlag==True & marFlag==True :
                            try:
                                duplicate_doc = False
                                #----------- check duplicate
                                for i in range(len(doctor_list_exist)):
                                    myRowData = doctor_list_exist[i]
                                    str1DocId = myRowData['doc_id']
                                    if (str(str1DocId).strip() == doc_id):
                                        duplicate_doc = True
                                        break
    
                                #-----------------
                                if(duplicate_doc == False):
                                    if doc_id not in excelList:
                                        excelList.append(doc_id)
    
                                        randNumber = randint(1001, 9999)
    
                                        # Create insert list
                                        ins_dict = {'cid':c_id, 'doc_id':doc_id, 'doc_name':doc_name, 'specialty':specialty,'degree':degree,'attached_institution':attachInstitute,'designation':designation,'dob':dob,'mar_day':mar_day,'password':randNumber, 'mobile':mobile, 'doctors_category':doctorsCategory, 'status':status}
                                        ins_list.append(ins_dict)
                                        count_inserted += 1
                                    else:
                                        error_data = row_data + '(duplicate in excel!)\n'
                                        error_str = error_str + error_data
                                        count_error += 1
                                        continue
                                else:
                                    error_data = row_data + '(duplicate Doctor ID)\n'
                                    error_str = error_str + error_data
                                    count_error += 1
                                    continue
    
                            except:
                                error_data = row_data + '(error in process)\n'
                                error_str = error_str + error_data
                                count_error += 1
                                continue
                        else:
                            error_data = row_data + '(Invalid DOB or Marriage day)\n'
                            error_str = error_str + error_data
                            count_error += 1
                            continue
                    else:
                        error_data = row_data + '(Invalid mobile)\n'
                        error_str = error_str + error_data
                        count_error += 1
                        continue
                else:
                    error_data = row_data + '(Doctor ID and Name needed)\n'
                    error_str = error_str + error_data
                    count_error += 1
                    continue
            else:
                error_data = row_data + '(10 columns need in a row)\n'
                error_str = error_str + error_data
                count_error += 1
                continue

        if error_str == '':
            error_str = 'No error'

        if len(ins_list) > 0:
            inCountList = db.sm_doctor.bulk_insert(ins_list)


    return dict(count_inserted=count_inserted, count_error=count_error, error_str=error_str, total_row=total_row)



        
def microunion():
    task_id='rm_reparea_manage'
    task_id_view='rm_reparea_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))

    cid=session.cid
    response.title='Microunion'

    #----------delete rep area---
    btn_delete=request.vars.btn_delete    
    if btn_delete:
        id_delete=request.vars.record_id
        db((db.sm_microunion.id == id_delete)).delete()

    
    microunion_area=str(request.vars.microunion_area).upper()
    microunion_id = str(request.vars.microunion_id).upper()

    microunion_name = str(request.vars.microunion_name).upper()
    
    # reqPage=len(request.args)

    try: 
        area_id=microunion_area.split('|')[0]
        area_name=microunion_area.split('|')[1]   
    except:
        area_id = str(request.vars.microunion_area).upper()
        area_name =''
        
    # return area_id
    level_area_sql = "select level0, level0_name, level1, level1_name, level2, level2_name, level3, level3_name  from sm_level where level_id = '"+area_id+"' limit 0, 1"
    # return level_area_sql
    level_area = db.executesql(level_area_sql, as_dict = True)
    if len(level_area) == 0:
        session.flash = 'Please Select Valid Pocket Market Area'
    else:
        for j in range(len(level_area)):
            records_level_dict=level_area[j]  
            level0=str(records_level_dict["level0"])            
            level0_name=str(records_level_dict["level0_name"])            
            level1=str(records_level_dict["level1"])      
            level1_name=str(records_level_dict["level1_name"])
            level2=str(records_level_dict["level2"])
            level2_name=str(records_level_dict["level2_name"])
            level3=str(records_level_dict["level3"])
            level3_name=str(records_level_dict["level3_name"])

        if microunion_id!='' and microunion_id!=None and microunion_id!='NONE' and microunion_name!='' and microunion_name!=None and  microunion_name!='NONE':
            check_sql = "select microunion_id, microunion_name from sm_microunion where microunion_id = '"+microunion_id+"' limit 0, 1"
            # return check_sql
            check = db.executesql(check_sql, as_dict = True)
            if len(check) > 0:
                response.flash = 'Already exist'
            else:
                insert_sql = "INSERT INTO sm_microunion(cid, microunion_id,  microunion_name, area_id, area_name, level0, level0_name, level1, level1_name, level2, level2_name, level3, level3_name, note) VALUES ('"+str(cid)+"','"+str(microunion_id)+"','"+str(microunion_name)+"','"+str(area_id)+"','"+str(area_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"', '')"
                # return insert_sql
                insert_str = db.executesql(insert_sql)
                session.flash = 'Submitted Successfully'
                redirect (URL('doctor','microunion'))
    # form.vars.area_id=area_id
    # form.vars.area_name=area_name 

    #     existRows = db((db.sm_microunion.cid == cid) & (db.sm_microunion.microunion_id == microunion_id) ).select(db.sm_microunion.microunion_id, limitby=(0, 1))
    #     if existRows:
    #         response.flash = 'Already exist'
    #     else:                        
    #         if form.accepts(request.vars,session,):
    #             response.flash = 'Submitted Successfully'

    # ----------Filter--------------
    btn_filter_target_microunion = request.vars.btn_filter_target_microunion
    btn_all = request.vars.btn_all
    reqPage = len(request.args)

    if btn_filter_target_microunion:
        session.btn_filter_target_microunion=btn_filter_target_microunion
        session.search_pocket_market=request.vars.search_pocket_market
        session.search_pocket_area_id_name=request.vars.search_pocket_area_id_name

        reqPage=0

    elif btn_all:
        session.btn_filter_target_microunion=None
        session.search_pocket_market=None
        session.search_pocket_area_id_name=None

        reqPage=0

    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging   

    qset = db()
    qset = qset(db.sm_microunion.cid == cid)

    if (session.btn_filter_target_microunion!=None and session.search_pocket_market!=None and session.search_pocket_market!=''):
        search_pocket_market=str(session.search_pocket_market).split('|')[0]        
        qset=qset(db.sm_microunion.microunion_id==search_pocket_market.upper())    


    if (session.btn_filter_target_microunion!=None and session.search_pocket_area_id_name!=None and session.search_pocket_area_id_name!=''):
        search_pocket_area_id_name=str(session.search_pocket_area_id_name).split('|')[0]        
        qset=qset(db.sm_microunion.area_id==search_pocket_area_id_name)


    records = qset.select(db.sm_microunion.ALL, orderby=db.sm_microunion.microunion_name, limitby=limitby)

    recordsCount=qset.count() 

    return dict(records=records,recordsCount=recordsCount,page=page,items_per_page=items_per_page,access_permission=access_permission)


def microunion_edit():
    response.title='Microunion Edit'
    
    #Check access permission
       #----------Task assaign----------
    task_id='microunion_manage'
    task_id_view='microunion_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('doctor','microunion'))
    
    c_id=session.cid

    #----------
    #   depot_combo

#    if (session.user_type=='Admin'):
#        rec_depot_combo=db((db.sm_depot.cid==session.cid)).select(db.sm_depot.depot_id,db.sm_depot.name,orderby=db.sm_depot.name)
#    elif (session.user_type=='Depot'):
#        rec_depot_combo=db((db.sm_depot.cid==session.cid) & (db.sm_depot.depot_id==session.depot_id)).select(db.sm_depot.depot_id,db.sm_depot.name,orderby=db.sm_depot.name)
#    else:
#        rec_depot_combo=db((db.sm_depot.cid==session.cid)).select(db.sm_depot.depot_id,db.sm_depot.name,orderby=db.sm_depot.name)
    
    
#    show_List=[]
#    for row in rec_depot_combo:
#        depot_id=row.depot_id
#        depot_name=row.name
#        
#        dictData= {'depot_id':depot_id,'depot_name': depot_name}
#        show_List.append(dictData)
#======================
   
    page= request.args(0)
    record= db.sm_microunion(request.args(1)) #or redirect(URL('index'))   

    form =SQLFORM(db.sm_microunion,
                  record=record,
                  deletable=True,
                  fields=['microunion_id','microunion_name'],
                  submit_button='Update'
                  )
    
    records_microunion=db((db.sm_microunion.cid==session.cid) & (db.sm_microunion.id==request.args(1))).select(db.sm_microunion.microunion_name,limitby=(0,1))
    sm_microunion=''
    for records_show_id in records_microunion :
         microunion_id=records_show_id.microunion_id
         break
    
    if form.accepts(request.vars, session):
        microunion_name=form.vars.microunion_name
        db((db.sm_microunion.cid==session.cid) & (db.sm_microunion.microunion_id==microunion_id)).update(microunion_name=microunion_name)
        return db._lastsql
        session.flash = 'Update Successfully'
        redirect(URL('rep',args=[page]))
    
    #If rep exist in rep area useflag will true
    useFlag=False
    repareaRows=db((db.sm_rep_area.cid==session.cid) & (db.sm_rep_area.rep_id==rep_id)).select(db.sm_rep_area.rep_id,orderby=db.sm_rep_area.rep_id,limitby=(0,1))
    if repareaRows:
        useFlag=True
    #------------------
    
    return dict(form=form,rep_id=rep_id,useFlag=useFlag,page=page)



#------------------rep end----------------------
def microunion_update():

    response.title='Microunion Edit'
    record_id = request.args(0)
    # return record_id
    # return record_poi_id
    microunion_select_sql = "select id, microunion_id, microunion_name, area_id, area_name from sm_microunion where id = '"+record_id+"'; "
    # return microunion_select_sql
    microunion_select = db.executesql(microunion_select_sql,as_dict=True)
    
    for i in range(len(microunion_select)):
        records_ov_dict=microunion_select[i]  
        # record_poi_id=str(records_ov_dict["id"])
        microunion_id=str(records_ov_dict["microunion_id"])            
        microunion_name=str(records_ov_dict["microunion_name"])            
        area_id=str(records_ov_dict["area_id"])      
        area_name=str(records_ov_dict["area_name"])
                    
        

    update_btn=request.vars.update_btn

    if update_btn:
        record_poi_id = request.args(0)
        # return record_poi_id
        # poi_id = str(request.vars.poi_id).strip()
        microunion_id = str(request.vars.microunion_id).strip()
        microunion_name = str(request.vars.microunion_name).strip()
        area_id = str(request.vars.area_id).strip()
        area_name = str(request.vars.area_name).strip().upper()
        # return session.mobile 
        # return area_id

        level_area_sql = "select level0, level0_name, level1, level1_name, level2, level2_name, level3, level3_name  from sm_level where level_id = '"+area_id+"' limit 0, 1"
        # return level_area_sql
        level_area = db.executesql(level_area_sql, as_dict = True)
        if len(level_area) == 0:
            session.flash = 'Pocket Market Area does not exits.'
            redirect(URL('doctor','microunion'))
        else:
            for j in range(len(level_area)):
                records_level_dict=level_area[j]  
                level0=str(records_level_dict["level0"])            
                level0_name=str(records_level_dict["level0_name"])            
                level1=str(records_level_dict["level1"])      
                level1_name=str(records_level_dict["level1_name"])
                level2=str(records_level_dict["level2"])
                level2_name=str(records_level_dict["level2_name"])
                level3=str(records_level_dict["level3"])
                level3_name=str(records_level_dict["level3_name"])

        update_microunion_sql= " Update sm_microunion Set  microunion_name= '"+str(microunion_name)+"', area_id ='"+str(area_id)+"', area_name ='"+str(area_name)+"',  level0= '"+str(level0)+"', level0_name ='"+str(level0_name)+"', level1 ='"+str(level1)+"',  level1_name= '"+str(level1_name)+"', level2 ='"+str(level2)+"', level2_name ='"+str(level2_name)+"', level3 ='"+str(level3)+"', level3_name ='"+str(level3_name)+"' WHERE id = '"+str(record_id)+"'  "  
        # return update_microunion_sql
        update_microunion = db.executesql(update_microunion_sql)
        session.flash = 'Microunion Updated Successfully'
        redirect(URL('doctor','microunion'))
    return dict(record_id = record_id, microunion_id = microunion_id,microunion_name=microunion_name,area_id=area_id,area_name=area_name )




def microunionDelete():
    c_id=session.cid
    recId=request.args[0]
    deleteRows = db((db.sm_microunion.cid == c_id) & (db.sm_microunion.id == recId)).delete()
    if  deleteRows:
        response.flash = 'Deleted Successfully'
               
    redirect (URL('microunion'))


def microunionDownload():
    c_id = session.cid
    qset=db()
    qset = qset(db.sm_microunion.cid == c_id)
    records = qset.select(db.sm_microunion.ALL, orderby=db.sm_microunion.area_name|db.sm_microunion.microunion_name, groupby=db.sm_microunion.microunion_id|db.sm_microunion.microunion_name)
    
#     return records
    myString='Microunion \n\n'
    myString+='Microunion ID,Microunion Name,BaseCode,BaseCode Name\n'
    for rec in records:
        microunion_id=str(rec.microunion_id)
        microunion_name=str(rec.microunion_name).replace(',', ' ')
        area_id=str(rec.area_id)
        area_name=str(rec.area_name).replace(',', ' ')
        
        
        myString+=microunion_id+','+microunion_name+','+area_id+','+area_name+'\n'
        
    #-----------
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_microunion.csv'   
    return str(myString)


def microunion_batch_upload():
   
    response.title = 'Microunion Batch Upload'

    c_id = session.cid
    btn_upload=request.vars.btn_upload
    btn_delete=request.vars.btn_delete
    
    count_inserted=0
    count_error=0
    error_str=''
    total_row=0
    
    # if btn_delete:
    #     delete_check=request.vars.delete_check
    #     if delete_check!='YES':
    #         response.flash='Confirmation Required'            
    #     else:
    #         db.district.truncate()
    #         db.district_thana.truncate()     
    #         response.flash='ALL Chart ID cleaned successfully'
            
    if btn_upload=='Upload':        
        excel_data=str(request.vars.excel_data)
        inserted_count=0
        error_count=0
        
        row_list=excel_data.split( '\n')
        total_row=len(row_list)
        
        area_id_list_exist=[]   
        
        area_id_list_excel=[]
                
        ins_list=[]
        ins_dict={}

        # ----------------------
        for i in range(total_row):
            if i>=500:
                break
            else:
                row_data=row_list[i]                    
                coloum_list=row_data.split( '\t')
                if len(coloum_list)==2:
                    areaIDExcel=str(coloum_list[0]).strip().upper()
                    
                    if areaIDExcel!='':
                        if areaIDExcel not in area_id_list_excel:
                            area_id_list_excel.append(areaIDExcel)

        #----------------------

        areaIDRows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id.belongs(area_id_list_excel)) ).select(db.sm_level.level_id,orderby=db.sm_level.level_id)
        area_id_list_exist=areaIDRows.as_list()

        #----------------------

        for i in range(total_row):
            if i>=100:
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
                micro_idExcel = str(coloum_list[0]).strip().upper()
                micro_nameExcel = str(coloum_list[1]).strip().upper()
                area_idExcel = str(coloum_list[2]).strip().upper()
                area_nameExcel = str(coloum_list[3]).strip().upper()
                # statusExcel = str(coloum_list[3]).strip()
                    
                if micro_idExcel=='' or area_idExcel=='':
                    error_data=row_data+'(Required all value)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
                # ------------------------------------------------------------------------
                try:
                    valid_area_id=False
                      
                    #Check valid item_list                         
                    for i in range(len(area_id_list_exist)):
                        myRowData=area_id_list_exist[i]                                
                        area_id=myRowData['area_id']
                        if (str(area_id).strip()==str(area_idExcel).strip()):
                            valid_area_id=True
                            break
                    
                    #-----------------
                    if valid_area_id==True:
                        error_data=row_data+'(Invalid Area ID/Name)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue

                # ---------------------------------------------------------------------------              
                    else:
                        AreaExistCheckRows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==area_idExcel)).select(db.sm_level.id,limitby=(0,1))
                        if not AreaExistCheckRows:
                            error_data=row_data+'(Please Select Valid Area ID/Name)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue
                        else:
                            existCheckRows=db((db.sm_microunion.cid==c_id)&(db.sm_microunion.microunion_id==micro_idExcel)).select(db.sm_microunion.id,limitby=(0,1))
                            if existCheckRows:
                                error_data=row_data+'(Duplicate Microunion ID)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue
                            else:
                                db.sm_microunion.insert(cid=c_id,microunion_id=micro_idExcel,microunion_name=micro_nameExcel,area_id=area_idExcel,area_name=area_nameExcel)
                                count_inserted+=1
                except:
                    error_data=row_data+'(error in process!)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
                                
        if error_str=='':
            error_str='No error'
    
    return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)


def microunionList():
    c_id=session.cid
    qset = db()
    qset = qset(db.sm_microunion.cid == c_id)
    records = qset.select(db.sm_microunion.ALL, orderby=db.sm_microunion.microunion_name)      
#     return records
    microunionList=''
    for record in records:
        if microunionList=='':
            microunionList=str(record.microunion_name).upper()+'|'+str(record.microunion_id).upper()
        else:
            microunionList=microunionList+','+str(record.microunion_name).upper()+'|'+str(record.microunion_id).upper()
            
    return microunionList

def get_territory():
    reiStr=''
    c_id = session.cid
    
    
    records=db((db.sm_level.cid == c_id) &(db.sm_level.depth == 3)).select(db.sm_level.level_id, db.sm_level.level_name, orderby=db.sm_level.level_name)
    # return records
    for row in records:
        level_id=str(row.level_id).replace('|', ' ').replace(',', ' ')
        level_name=str(row.level_name).replace('|', ' ').replace(',', ' ')
        
        if reiStr=='':
            reiStr=level_id+'|'+level_name
        else:
            reiStr+=','+level_id+'|'+level_name
        
        
    return reiStr


def get_pocket_market_idName():
    reiStrMarket=''
    c_id = session.cid
    
    
    records=db((db.sm_microunion.cid == c_id) ).select(db.sm_microunion.microunion_id, db.sm_microunion.microunion_name, orderby=db.sm_microunion.microunion_name)
    # return records
    for row in records:
        microunion_id=str(row.microunion_id).replace('|', ' ').replace(',', ' ')
        microunion_name=str(row.microunion_name).replace('|', ' ').replace(',', ' ')
        
        if reiStrMarket=='':
            reiStrMarket=microunion_id+'|'+microunion_name
        else:
            reiStrMarket+=','+microunion_id+'|'+microunion_name
        
        
    return reiStrMarket
