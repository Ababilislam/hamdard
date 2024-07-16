
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
    
    if (session.btn_filter_doctor):
        if (session.searchType_doctor == 'DocID'):
            searchValue=str(session.searchValue_doctor).split('|')[0]            
            qset = qset(db.sm_doctor.doc_id == searchValue)
            
        elif (session.searchType_doctor == 'Specialty'):            
            qset = qset(db.sm_doctor.specialty == session.searchValue_doctor)
            
        elif (session.searchType_doctor == 'Status'):
            qset = qset(db.sm_doctor.status == session.searchValue_doctor)
            
        elif (session.searchType_doctor == 'UpdatedBy'):
            qset = qset(db.sm_doctor.updated_by == session.searchValue_doctor)
            
    records = qset.select(db.sm_doctor.ALL, orderby=db.sm_doctor.doc_id, limitby=limitby)
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
    if (session.btn_filter_doctor):
        if (session.searchType_doctor == 'DocID'):
            searchValue=str(session.searchValue_doctor).split('|')[0]            
            qset = qset(db.sm_doctor.doc_id == searchValue)
            
        elif (session.searchType_doctor == 'Specialty'):            
            qset = qset(db.sm_doctor.specialty == session.searchValue_doctor)
            
        elif (session.searchType_doctor == 'Status'):
            qset = qset(db.sm_doctor.status == session.searchValue_doctor)
    else:
        session.flash = 'Filter Required'
        redirect (URL('doctor_list'))
    
    records = qset.select(db.sm_doctor.ALL, orderby=db.sm_doctor.doc_name)


    #---------
    myString = 'Doctor List\n\n'
    myString += 'Doctor ID,Name,Specialty,Degree,Chamber Address, Attach Institute,Designation,DOB,Mobile,Doctors Category,Status,Updated By\n'
    for rec in records:
        docId = str(rec.doc_id)
        docName = str(rec.doc_name).replace(',', ' ')
        specialty = str(rec.specialty).replace(',', '; ')
        degree = str(rec.field1).replace(',', '; ')
        chamberAddress = str(rec.des).replace(',', '; ')
        attachInstitute = str(rec.attached_institution).replace(',', '; ')
        designation = str(rec.designation).replace(',', '; ')
        dob = str(rec.dob)          
        mobile = str(rec.mobile)
        doctorsCategory = str(rec.doctors_category).replace(',', '; ')
        status = str(rec.status)
        updated_by = str(rec.updated_by)
        
        if int(mobile) == 0:
            mobile = ''
        if dob == 'None':
            dob = ''
            
        myString += docId + ',' + docName + ',' + specialty+ ',' + degree + ',' + chamberAddress + ',' + attachInstitute + ',' + designation + ',' + dob + ',' + mobile + ',' + doctorsCategory + ',' + status + ',' + updated_by + '\n'

    #-----------
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
    c_id=session.cid
    response.title='Microunion'
    
    microunion_area=str(request.vars.microunion_area).upper()
    microunion_id = str(request.vars.microunion_id).upper()
    microunion_name = str(request.vars.microunion_name).upper()
#     return microunion_area
    area_id=''
    area_name=''
    if microunion_area!='' and microunion_area!=None and microunion_area!='NONE':
        area_id=microunion_area.split('|')[0]
        area_name=microunion_area.split('|')[1]
    
#     return area_id
    if microunion_id!='' and microunion_id!=None and microunion_id!='NONE' and microunion_name!='' and microunion_name!=None:
        existRows = db((db.sm_microunion.cid == c_id) & (db.sm_microunion.microunion_id == microunion_id) & (db.sm_microunion.microunion_name == microunion_name)).select(db.sm_microunion.microunion_id, limitby=(0, 1))
        if existRows:
            response.flash = 'Already exist'
        else:
            insRes = db.sm_microunion.insert(cid=c_id, microunion_id=microunion_id, microunion_name=microunion_name,area_id=area_id,area_name=area_name)
            if insRes:
                response.flash = 'Submitted Successfully'
    qset = db()
    qset = qset(db.sm_microunion.cid == c_id)
    records = qset.select(db.sm_microunion.ALL, orderby=db.sm_microunion.microunion_name)            
    return dict(records=records)

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
